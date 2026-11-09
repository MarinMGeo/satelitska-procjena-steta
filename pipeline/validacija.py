"""
Procjena pouzdanosti analize poplave i tuče (EUPL-1.2).

Bez terenskog očevida nema "prave" istine na terenu, pa se točnost procjenjuje neovisnim izvorima:
  POPLAVA: radar Sentinel-1 (17. 5.) prema optici Sentinel-2 (nova voda ili mokro tlo 22. 5.), po pikselima i po parcelama;
           kontrolni test: koliko nepoplavljenih parcela ima jednako jak pad vegetacije (lažni alarm);
           osjetljivost na prag (blago / pravilo / strogo).
  TUČA:    klase iz NDVI-ja prema klasama iz neovisnih pojaseva (NDMI = B8A/B11, NDRE = B8A/B05);
           osjetljivost na izbor referentnih parcela; položaj prijave tuče ESWD prema pojasu.
Rezultat: validacija.json za aplikaciju.

Pokretanje:  python validacija.py <S2_poplava_SAFE_mapa> <ulaz_poplava> <izlaz_poplava> <docs/data> <izlaz_tuca/pojas_tuce.gpkg>
"""
import sys, json, glob, pathlib
import numpy as np, pyogrio, rasterio, geopandas as gpd
from rasterio.warp import reproject, Resampling
from rasterio.transform import from_origin
from rasterio.features import rasterize
from shapely.geometry import Point

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from izvoz_web_podataka_lib import qgis_poplava  # noqa

S2DIR, ULAZ, QOUT, OUT = map(pathlib.Path, sys.argv[1:5])
CRS = "EPSG:3765"


def cm2(a, b):
    """2x2 matrica (a = procjena, b = referenca) i pokazatelji."""
    tp = int((a & b).sum()); fp = int((a & ~b).sum()); fn = int((~a & b).sum()); tn = int((~a & ~b).sum())
    n = tp + fp + fn + tn; oa = (tp + tn) / n
    pe = ((tp + fp) * (tp + fn) + (fn + tn) * (fp + tn)) / n / n
    kappa = (oa - pe) / (1 - pe) if pe < 1 else 0
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn, "oa": oa, "kappa": kappa,
            "preciznost": tp / (tp + fp) if tp + fp else None, "odziv": tp / (tp + fn) if tp + fn else None}


def kappa_k(m):
    m = np.asarray(m, float); n = m.sum(); po = np.trace(m) / n; pe = (m.sum(0) * m.sum(1)).sum() / n / n
    return (po - pe) / (1 - pe)


V = {}
# ======================= POPLAVA =======================
det, dt10, VV, par = qgis_poplava(ULAZ, QOUT)
(v5, t5), (v17, t17), (v29, t29) = VV["05"], VV["17"], VV["29"]
H10, W10 = v17.shape; RES = 20.0; W, H = W10 // 2, H10 // 2; T = from_origin(t17.c, t17.f, RES, RES)


def band(date, name):
    f = glob.glob(str(S2DIR / f"**/*_{date}T*_{name}_20m.jp2"), recursive=True)[0]
    with rasterio.open(f) as s:
        d = np.zeros((H, W), np.float32)
        reproject(rasterio.band(s, 1), d, dst_transform=T, dst_crs=CRS,
                  resampling=Resampling.nearest if name == "SCL" else Resampling.bilinear, src_nodata=0, dst_nodata=0)
    return d


def to20(a, t, resamp=Resampling.average):
    d = np.full((H, W), np.nan, np.float32)
    reproject(np.nan_to_num(a, nan=0) if resamp == Resampling.average else a, d, src_transform=t, src_crs=CRS, dst_transform=T, dst_crs=CRS, resampling=resamp)
    return d


refl = lambda dn: np.where(dn > 0, (dn - 1000.0) / 10000.0, np.nan)
nd = lambda a, b: np.where((a + b) != 0, (a - b) / (a + b), np.nan)
S = {}
for k, d in {"05": "20230505", "22": "20230522"}.items():
    scl = band(d, "SCL"); ok = (scl > 0) & ~np.isin(scl, [0, 1, 3, 8, 9, 10, 11])
    m = nd(refl(band(d, "B03")), refl(band(d, "B11"))); nv = nd(refl(band(d, "B8A")), refl(band(d, "B04")))
    S[k] = {"ok": ok, "wet": ok & ((m > 0) | (scl == 6)), "ndvi": np.where(ok, nv, np.nan)}
flood = to20(det, dt10) >= 0.5

lab = rasterize(((g, i + 1) for i, g in enumerate(par.geometry)), out_shape=(H, W), transform=T, fill=0, dtype="int32")
inA = lab > 0
both = inA & S["05"]["ok"] & S["22"]["ok"]
new_wet = S["22"]["wet"] & ~S["05"]["wet"]
px = cm2(flood[both], new_wet[both])
px["ha_po_pikselu"] = RES * RES / 1e4
V["poplava_pikseli"] = px

# po parcelama: radar poplavljeno (>=10 % parcele) prema optičkom signalu (nova voda/mokro na >=10 % ili značajan pad NDVI-ja)
n = len(par) + 1


def zsum(mask, w=None):
    m = mask & (lab > 0)
    return np.bincount(lab[m], weights=None if w is None else w[m], minlength=n)


cnt = zsum(both)
wetf = np.divide(zsum(both & new_wet), cnt, out=np.zeros(n), where=cnt > 0)
v_ok = both & ~np.isnan(S["05"]["ndvi"]) & ~np.isnan(S["22"]["ndvi"])
c2 = zsum(v_ok)
dnd = np.divide(zsum(v_ok, S["22"]["ndvi"] - S["05"]["ndvi"]), c2, out=np.full(n, np.nan), where=c2 > 0)
lu = np.r_[0, par.land_use_i.fillna(0).astype(int).values]
fpct = np.r_[0, par.posto_poplavljenosti.fillna(0).values]
s1 = fpct >= 10
s1_none = np.r_[0, par.poplava_ha.fillna(0).values] == 0
z = np.full(n, np.nan)
for u in np.unique(lu[1:]):
    sel = (lu == u) & s1_none & ~np.isnan(dnd) & (c2 >= 3)
    if sel.sum() >= 30:
        med = np.median(dnd[sel]); mad = max(np.median(np.abs(dnd[sel] - med)) * 1.4826, 0.02)
        z[lu == u] = (dnd[lu == u] - med) / mad
valid = (c2 >= 3) & ~np.isnan(z)
valid[0] = False
opt_sig = (wetf >= 0.10) | (z < -2)
eval_set = valid & (s1 | s1_none)  # isključene parcele s 0-10 % poplave (granični slučajevi)
pc = cm2(s1[eval_set], opt_sig[eval_set])
pc["napomena"] = "radar: >=10 % parcele poplavljeno; optika: >=10 % nove vode/mokrog tla 22. 5. ili pad NDVI-ja z < -2"
V["poplava_parcele"] = pc
V["poplava_lazni_alarm_kontrola"] = float((opt_sig & s1_none & valid).sum() / max(1, (s1_none & valid).sum()))

# osjetljivost na prag (10 m)
def rule(t1, t2, t3=None):
    off = lambda a, t: a  # rasteri iste mreže uz pomak do pola piksela
    a5 = v5[:, :]; r = np.zeros_like(v17, bool)
    h = min(v5.shape[0], v17.shape[0], v29.shape[0]); w = min(v5.shape[1], v17.shape[1], v29.shape[1])
    x5, x17, x29 = v5[:h, :w], v17[:h, :w], v29[:h, :w]
    m = (x17 < t1) & ((x17 - x5) < t2)
    if t3 is not None: m &= (x29 - x17) > t3
    return float(np.nansum(m) * 0.01)
V["poplava_prag"] = {"blago (-14 / -2)": rule(-14, -2), "pravilo (-16 / -3 / +3)": rule(-16, -3, 3), "strogo (-19 / -5)": rule(-19, -5),
                     "pravilo bez uvjeta povlačenja": rule(-16, -3)}
print(json.dumps({k: V[k] for k in V}, indent=1, default=float))

# ======================= TUČA =======================
T_ = json.load(open(OUT / "tuca" / "parcele.json")); F = T_["fields"]
P = [dict(zip(F, a)) for a in T_["props"]]
kl = np.array([p["kl"] for p in P]); pj = np.array([p["pojas"] or 0 for p in P])
assessed = kl >= 0
def dz(ix):
    d = np.array([(p[ix + "_poslije"] - p[ix + "_prije"]) if p[ix + "_poslije"] is not None and p[ix + "_prije"] is not None else np.nan for p in P])
    ref = assessed & (pj == 0) & ~np.isnan(d)
    med = np.median(d[ref]); mad = np.median(np.abs(d[ref] - med)) * 1.4826
    return (d - med) / mad, d
out = {}
dmg = kl >= 1
for ix in ["NDMI", "NDRE"]:
    zz, _ = dz(ix); ok = assessed & ~np.isnan(zz)
    out[ix] = cm2(dmg[ok], (zz < -1)[ok])
V["tuca_indeksi"] = out
# isti mjerni okvir za sve indekse: referenca = oranice izvan pojasa tuče
dN, _ = dz("NDVI")
out2 = {}
for ix in ["NDMI", "NDRE"]:
    zz, _ = dz(ix); ok = assessed & ~np.isnan(zz) & ~np.isnan(dN)
    out2[ix] = cm2((dN < -1)[ok], (zz < -1)[ok])
V["tuca_indeksi_ista_referenca"] = out2
ha = np.array([p["ha"] for p in P]); n0 = np.array([p["NDVI_prije"] if p["NDVI_prije"] is not None else np.nan for p in P])
dd = np.array([p["dndvi"] if p["dndvi"] is not None else np.nan for p in P]); r2 = T_["ref_izvan_pojasa"]
zz2 = (dd - r2["med"]) / r2["mad"]
kk = lambda sel: np.where(sel, np.clip(-(dd - r2["med"]) / np.maximum(n0, 0.15), 0, 1), 0)
V["tuca_raspon"] = {"ha_sve": float(ha[kl >= 1].sum()), "ha_izvan_pojasa": float(ha[assessed & (zz2 <= -1)].sum()),
                    "eur_sve_kukuruz": float(np.nansum(ha * 7.7 * 177.59 * kk(kl >= 1))),
                    "eur_izvan_pojasa_kukuruz": float(np.nansum(ha * 7.7 * 177.59 * kk(assessed & (zz2 <= -1))))}
# klase: referenca sve ocijenjene oranice prema referenci izvan pojasa
ref2 = T_["ref_izvan_pojasa"]
d = np.array([p["dndvi"] if p["dndvi"] is not None else np.nan for p in P])
z2 = (d - ref2["med"]) / ref2["mad"]
kl2 = np.where(z2 <= -3, 3, np.where(z2 <= -2, 2, np.where(z2 <= -1, 1, 0)))
m = np.zeros((4, 4), int)
for a, b in zip(kl[assessed], kl2[assessed]): m[a, b] += 1
V["tuca_referenca_matrica"] = {"redovi_sve_stupci_izvan_pojasa": m.tolist(), "kappa": kappa_k(m), "podudarnost": float(np.trace(m) / m.sum())}
# ESWD prema pojasu
poj = pyogrio.read_dataframe(sys.argv[5]) if len(sys.argv) > 5 else None
meta = json.load(open(OUT / "tuca" / "meta.json"))
if poj is not None:
    pt = gpd.GeoSeries([Point(e["lon"], e["lat"]) for e in meta["eswd"]], crs=4326).to_crs(poj.crs)
    V["tuca_eswd_udaljenost_m"] = [float(poj.distance(p).min()) for p in pt]
print(json.dumps({k: V[k] for k in V if k.startswith("tuca")}, indent=1, default=float))
json.dump(V, open(OUT / "validacija.json", "w"), default=float)
