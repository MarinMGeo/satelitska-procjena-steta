"""
Optički dio analize poplave: Sentinel-2 L2A (12. 5. 2022., 5. 5. 2023., 22. 5. 2023.).

Nadopunjuje radarsku (Sentinel-1) detekciju:
  1) potvrđuje vodu i mokro tlo pet dana nakon vrhunca poplave (MNDWI),
  2) mjeri stanje vegetacije prije i poslije poplave (NDVI) i iz toga daje
     koeficijent gubitka prinosa za svaku poplavljenu ARKOD parcelu,
  3) izrađuje prikazne podloge u prirodnim bojama za web aplikaciju.

Ispravke u odnosu na prvu probnu verziju:
  - od refleksije se oduzima BOA_ADD_OFFSET (-1000) za procesnu verziju N0400+,
  - maska oblaka uklanja samo SCL 0, 1, 3, 8, 9, 10, 11 (voda i neklasificirano ostaju),
  - NDVI = (B8A - B04) / (B8A + B04), voda iz NDVI-ja se ne izvodi,
  - sve se računa samo za područje istraživanja.

Pokretanje:
    python optika_sentinel2.py <mapa_s_tri_SAFE_produkta> <ulaz_poplava> <izlaz_poplava (qgis_poplava.py)> <docs/data>

Licencija: EUPL-1.2
"""
import sys, json, glob, pathlib
import numpy as np, pyogrio, rasterio
from rasterio.warp import reproject, Resampling, calculate_default_transform
from rasterio.transform import from_origin
from rasterio.features import rasterize
from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from izvoz_web_podataka_lib import qgis_poplava  # noqa: E402

S2DIR, ULAZ, QOUT, OUT = map(pathlib.Path, sys.argv[1:5])
DATES = {"d22": "20220512", "d05": "20230505", "d22b": "20230522"}
LABEL = {"d22": "12. 5. 2022.", "d05": "5. 5. 2023.", "d22b": "22. 5. 2023."}
CRS = "EPSG:3765"
BAD_SCL = [0, 1, 3, 8, 9, 10, 11]

det, dt10, VV, par = qgis_poplava(ULAZ, QOUT)
vv, vvt = VV["17"]
H10, W10 = vv.shape
# radni raster: 20 m, isti obuhvat kao radarski
RES = 20.0
W, H = W10 // 2, H10 // 2
T = from_origin(vvt.c, vvt.f, RES, RES)


def band(date, name):
    f = glob.glob(str(S2DIR / f"**/*_{date}T*_{name}_20m.jp2"), recursive=True)
    if not f: raise FileNotFoundError(f"{date} {name}")
    with rasterio.open(f[0]) as src:
        dst = np.zeros((src.count, H, W), np.float32)
        for b in range(src.count):
            reproject(rasterio.band(src, b + 1), dst[b], dst_transform=T, dst_crs=CRS,
                      resampling=Resampling.nearest if name in ("SCL", "TCI") else Resampling.bilinear,
                      src_nodata=0, dst_nodata=0)
    return dst if src.count > 1 else dst[0]


refl = lambda dn: np.where(dn > 0, (dn - 1000.0) / 10000.0, np.nan)
nd = lambda a, b: np.where((a + b) != 0, (a - b) / (a + b), np.nan)

S = {}
for k, d in DATES.items():
    scl = band(d, "SCL")
    ok = (scl > 0) & ~np.isin(scl, BAD_SCL)
    b04, b8a = refl(band(d, "B04")), refl(band(d, "B8A"))
    ndvi = np.where(ok, nd(b8a, b04), np.nan)
    rec = {"ok": ok, "ndvi": ndvi, "scl": scl}
    if k != "d22":
        b03, b11 = refl(band(d, "B03")), refl(band(d, "B11"))
        rec["mndwi"] = np.where(ok, nd(b03, b11), np.nan)
    rec["tci"] = band(d, "TCI")
    S[k] = rec
    print(k, "bez oblaka:", round(ok.mean() * 100, 1), "%")

# radarska maska poplave na 20 m (udio poplavljenih 10 m piksela)
det20 = np.zeros((H, W), np.float32)
reproject(np.nan_to_num(det), det20, src_transform=dt10, src_crs=CRS, dst_transform=T, dst_crs=CRS, resampling=Resampling.average)
flood20 = det20 >= 0.5

# ---------- potvrda poplave optikom ----------
a = RES * RES / 1e4
m22 = S["d22b"]["mndwi"]; ok22 = S["d22b"]["ok"]
wet = (m22 > 0) | (S["d22b"]["scl"] == 6)
stats = {
    "s1_ha": float(flood20.sum() * a),
    "s1_vidljivo_ha": float((flood20 & ok22).sum() * a),
    "s1_voda_22_ha": float((flood20 & ok22 & wet).sum() * a),
    "s1_voda_05_ha": float((flood20 & S["d05"]["ok"] & (S["d05"]["mndwi"] > 0)).sum() * a),
    "oblaci_22_posto": float((~ok22).mean() * 100),
}
nd05, nd22b, nd22 = S["d05"]["ndvi"], S["d22b"]["ndvi"], S["d22"]["ndvi"]
both = flood20 & ~np.isnan(nd05) & ~np.isnan(nd22b)
ctrl = ~flood20 & (det20 == 0) & ~np.isnan(nd05) & ~np.isnan(nd22b)
stats["dndvi_poplava_median"] = float(np.median((nd22b - nd05)[both]))
stats["dndvi_kontrola_median"] = float(np.median((nd22b - nd05)[ctrl]))
print(json.dumps(stats, indent=1))

# ---------- po parcelama ----------
lab = rasterize(((g, i + 1) for i, g in enumerate(par.geometry)), out_shape=(H, W), transform=T, fill=0, dtype="int32")
n = len(par) + 1


def zmean(v, mask=None):
    m = ~np.isnan(v) & (lab > 0)
    if mask is not None: m &= mask
    s = np.bincount(lab[m], weights=v[m], minlength=n); c = np.bincount(lab[m], minlength=n)
    with np.errstate(invalid="ignore", divide="ignore"): return s / c, c


cnt_all = np.bincount(lab.ravel(), minlength=n)
r = {}
for k in DATES: r[k], r[k + "_n"] = zmean(S[k]["ndvi"])
r["d05f"], r["d05f_n"] = zmean(nd05, flood20)
r["d22bf"], r["d22bf_n"] = zmean(nd22b, flood20)
wet_s, _ = zmean(np.where(ok22, wet.astype(np.float32), np.nan), flood20)
cloud22, _ = zmean((~ok22).astype(np.float32))

# kontrolne (nepoplavljene) parcele iste vrste uporabe: normalna promjena NDVI-ja u istom razdoblju
d = r["d22b"] - r["d05"]
lu = np.r_[0, par.land_use_i.fillna(0).astype(int).values]
fl = np.r_[False, (par.fha > 0).values].astype(bool)
ref = {}
for u in np.unique(lu[1:]):
    sel = (lu == u) & ~fl & ~np.isnan(d) & (r["d22b_n"] >= 3) & (r["d05_n"] >= 3)
    if sel.sum() >= 30:
        med = float(np.median(d[sel])); mad = float(np.median(np.abs(d[sel] - med)) * 1.4826)
        ref[int(u)] = {"med": med, "mad": max(mad, 0.02), "n": int(sel.sum())}
allsel = ~fl & ~np.isnan(d)
ref_all = {"med": float(np.median(d[allsel])), "mad": float(np.median(np.abs(d[allsel] - np.median(d[allsel]))) * 1.4826)}
print("kontrola po vrsti uporabe:", ref)

out = []
for i in range(1, n):
    p = par.iloc[i - 1]
    if p.fha <= 0: continue
    u = int(p.land_use_i or 0); rr = ref.get(u, ref_all)
    # NDVI na poplavljenom dijelu parcele ako ima barem 2 piksela, inače cijela parcela
    usef = r["d05f_n"][i] >= 2 and r["d22bf_n"][i] >= 2
    n05 = r["d05f"][i] if usef else r["d05"][i]
    n22b = r["d22bf"][i] if usef else r["d22b"][i]
    k = z = None; why = ""
    if np.isnan(n05) or np.isnan(n22b):
        why = "oblaci"
    else:
        anom = (n22b - n05) - rr["med"]
        z = anom / rr["mad"]
        if u == 200 and n05 < 0.3:
            # oranica bez razvijenog usjeva 5. 5. (golo tlo, tek posijano): pad NDVI-ja ne može pokazati štetu
            why = "golo tlo"
        else:
            k = float(np.clip(-anom / max(n05, 0.15), 0, 1)) if z < -1 else 0.0
    f = lambda x: None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 3)
    out.append([int(p.id), f(r["d22"][i]), f(r["d05"][i]), f(r["d22b"][i]), f(n05), f(n22b),
                f(wet_s[i]) if usef else None, f(cloud22[i]), f(z), f(k), int(usef), why])

json.dump({"fields": ["id", "ndvi22", "ndvi05", "ndvi22b", "ndvi05f", "ndvi22bf", "voda22", "oblak22", "z", "k", "naPoplavi", "razlog"],
           "datumi": LABEL, "kontrola": {str(k): v for k, v in ref.items()}, "kontrola_sve": ref_all, "stats": stats, "rows": out},
          open(OUT / "optika.json", "w"), separators=(",", ":"))
ks = [o[9] for o in out if o[9] is not None]
print("parcela s koeficijentom:", len(ks), "od", len(out), "srednji k:", round(float(np.mean(ks)), 3))

# ---------- prikazne podloge (Web Mercator, isti okvir kao radarske) ----------
left, top = vvt.c, vvt.f; right, bottom = left + W10 * vvt.a, top + H10 * vvt.e
dtm, dw, dh = calculate_default_transform(CRS, "EPSG:3857", W10, H10, left, bottom, right, top, resolution=25)


def to3857(arr, resamp=Resampling.bilinear, nodata=np.nan):
    o = np.full((dh, dw), nodata, np.float32)
    reproject(arr.astype(np.float32), o, src_transform=T, src_crs=CRS, dst_transform=dtm, dst_crs="EPSG:3857",
              resampling=resamp, src_nodata=nodata, dst_nodata=nodata)
    return o


valid_area = to3857(np.where(np.isnan(vv[:H * 2:2, :W * 2:2]), np.nan, 1.0)) == 1
for k, nm in [("d22", "s2_20220512"), ("d05", "s2_20230505"), ("d22b", "s2_20230522")]:
    rgb = [to3857(S[k]["tci"][b], nodata=0) for b in range(3)]
    g = lambda x: np.clip(np.nan_to_num(x) * 1.15, 0, 255).astype(np.uint8)  # TCI je već 8-bitni, malo posvijetliti
    alpha = ((rgb[0] > 0) & valid_area).astype(np.uint8) * 255
    Image.fromarray(np.dstack([g(rgb[0]), g(rgb[1]), g(rgb[2]), alpha])).save(OUT / f"{nm}.webp", "WEBP", quality=74, method=6)

# karta promjene NDVI-ja (22. 5. - 5. 5. 2023.), divergentna paleta
dn = to3857(nd22b - nd05)
v = np.clip(dn / 0.4, -1, 1)
red = np.where(v < 0, 200, (1 - v) * 230 + v * 40); grn = np.where(v < 0, (1 + v) * 230 + (-v) * 40, 200 - v * 40)
blu = np.where(v < 0, (1 + v) * 230 + (-v) * 50, (1 - v) * 230 + v * 60)
alpha = np.where(np.isnan(dn) | ~valid_area, 0, np.clip(np.abs(v) * 255 * 1.6, 40, 230))
Image.fromarray(np.dstack([np.nan_to_num(c).astype(np.uint8) for c in (red, grn, blu)] + [alpha.astype(np.uint8)])).save(
    OUT / "s2_dndvi.webp", "WEBP", quality=80, method=6)

# voda/mokro tlo 22. 5. (MNDWI > 0 ili SCL voda), samo tamo gdje nema oblaka
wm = to3857(np.where(ok22, wet.astype(np.float32), np.nan), Resampling.nearest)
Image.fromarray(np.dstack([np.full(wm.shape, 40, np.uint8), np.full(wm.shape, 110, np.uint8), np.full(wm.shape, 255, np.uint8),
                           np.where(wm == 1, 210, 0).astype(np.uint8)])).save(OUT / "s2_voda_20230522.webp", "WEBP", quality=85, method=6)
cl = to3857((~ok22).astype(np.float32), Resampling.nearest)
Image.fromarray(np.dstack([np.full(cl.shape, 235, np.uint8)] * 3 + [np.where(cl == 1, 150, 0).astype(np.uint8)])).save(
    OUT / "s2_oblaci_20230522.webp", "WEBP", quality=80, method=6)
print("Gotovo.")
