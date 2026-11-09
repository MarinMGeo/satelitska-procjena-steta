"""
Tuča, Gradište, Županja i Štitar, 1. 7. 2024.: izvoz rezultata analize u QGIS-u (qgis_tuca.py) u web podatke.

Ulaz:
  <izlaz_qgis>/ARKOD_oranice_klase_stete.gpkg   oranice (unutarnji pojas -10 m): dNDVI, z, klasa, udio ispod praga, 6 indeksa
  <izlaz_qgis>/pojas_tuce.gpkg                  pojas tuče
  <izlaz_qgis>/dNDVI_oranice_bez_zetve.tif      dNDVI s maskiranom žetvom
  jls.geojson / .gpkg                           granice Gradišta, Županje i Štitara
  dvije Sentinel-2 L2A SAFE mape (TCI_20m, SCL_20m) za prikaz u prirodnim bojama

Pokretanje:
    python tuca_web.py <izlaz_qgis> <jls> <mapa_sa_SAFE> <izlaz>

Licencija: EUPL-1.2
"""
import sys, json, glob, pathlib
import numpy as np, pyogrio, rasterio, geopandas as gpd
from rasterio.warp import reproject, Resampling, calculate_default_transform
from pyproj import Transformer
from PIL import Image

Q, JLS, S2, OUT = map(pathlib.Path, sys.argv[1:5]); OUT.mkdir(parents=True, exist_ok=True)
CRS = "EPSG:3765"

par = pyogrio.read_dataframe(Q / "ARKOD_oranice_klase_stete.gpkg")
pojas = pyogrio.read_dataframe(Q / "pojas_tuce.gpkg")
jls = gpd.read_file(JLS).to_crs(CRS)
par["kl"] = par.klasa.astype(int)                       # -1 = žetva, nije ocijenjeno
par["MEAN"] = par.dNDVI_mean.where(par.dNDVI_count > 0)
par["udio"] = par.udio_mean.where(par.dNDVI_count > 0)

IND = ["NDVI", "NDRE", "NDMI", "MSAVI2", "PSRI", "BSI"]
Z = {f"{ix}_{t}": par[f"{ix}_{t}_mean"].astype(float).values for ix in IND for t in ("prije", "poslije")}

# ---------- reference: sve ocijenjene oranice (z u QGIS-u) i oranice izvan pojasa tuče ----------
ok = par.kl >= 0
mu, sd = float(par.MEAN[ok].mean()), float(par.MEAN[ok].std(ddof=0))
out_belt = ok & (par.udio == 0)
med = float(par.MEAN[out_belt].median()); mad = float((par.MEAN[out_belt] - med).abs().median() * 1.4826)
print(f"referenca sve oranice: {mu:.4f} / {sd:.4f} | izvan pojasa ({out_belt.sum()} parcela): medijan {med:.4f}, MAD {mad:.4f}")

# ---------- gubitak prinosa iz NDVI-ja ----------
nd0 = Z["NDVI_prije"]
anom = par.MEAN.values - med
k = np.where(par.kl.values >= 1, np.clip(-anom / np.maximum(np.nan_to_num(nd0, nan=0.15), 0.15), 0, 1), 0.0)
k = np.where(par.kl.values < 0, np.nan, k)

# ---------- JLS ----------
pts = par[["geometry"]].copy(); pts["geometry"] = par.geometry.representative_point()
jidx = gpd.sjoin(pts, jls[["geometry"]], how="left", predicate="within").index_right.fillna(-1).astype(int)
jidx = jidx[~jidx.index.duplicated()].reindex(par.index).fillna(-1).astype(int)


def enc(geom, scale=1e5):
    res = []
    for pg in ([geom] if geom.geom_type == "Polygon" else geom.geoms):
        rr = []
        for ring in [pg.exterior, *pg.interiors]:
            c = np.round(np.asarray(ring.coords)[:-1] * scale).astype(np.int64)
            if len(c) >= 3: rr.append(np.vstack([c[:1], np.diff(c, axis=0)]).ravel().tolist())
        if rr: res.append(rr)
    return res


p4 = par.copy(); p4["geometry"] = p4.geometry.simplify(1.0, preserve_topology=True); p4 = p4.to_crs(4326)
f = lambda x, d=3: None if x is None or not np.isfinite(x) else round(float(x), d)
props = []
for i, r in enumerate(p4.itertuples()):
    ha = (r.area if r.area and r.area > 0 else par.geometry.iloc[i].area) / 1e4    # površina ARKOD parcele
    props.append([int(r.id), round(ha, 4), int(r.kl), f(r.z, 2), f(r.MEAN, 4), f(r.udio, 3), int(r.dNDVI_count or 0),
                  r.home_name or "", int(jidx.iloc[i]), f(k[i])] + [f(Z[f"{ix}_{t}"][i]) for ix in IND for t in ("prije", "poslije")])
fields = ["id", "ha", "kl", "z", "dndvi", "pojas", "npx", "toponim", "j", "k"] + [f"{ix}_{t}" for ix in IND for t in ("prije", "poslije")]
json.dump({"fields": fields, "scale": 1e5, "jls": jls.JLS_IME_HR.tolist(), "props": props, "geoms": [enc(g) for g in p4.geometry],
           "ref_sve": {"med": mu, "sd": sd}, "ref_izvan_pojasa": {"med": med, "mad": mad, "n": int(out_belt.sum())}},
          open(OUT / "parcele.json", "w"), separators=(",", ":"))
pj = pojas.copy(); pj["geometry"] = pj.geometry.simplify(3, preserve_topology=True); pj = pj.to_crs(4326)
json.dump({"scale": 1e5, "props": [[round(a / 1e4, 3)] for a in pojas.area], "geoms": [enc(g) for g in pj.geometry]},
          open(OUT / "pojas.json", "w"), separators=(",", ":"))
j4 = jls.to_crs(4326); j4["geometry"] = j4.geometry.simplify(0.0002)
j4[["JLS_IME_HR", "geometry"]].to_file(OUT / "jls.geojson", driver="GeoJSON", COORDINATE_PRECISION=5)

# ---------- prikazne podloge, Web Mercator 20 m ----------
xmin, ymin, xmax, ymax = np.r_[np.minimum(jls.total_bounds[:2], par.total_bounds[:2]), np.maximum(jls.total_bounds[2:], par.total_bounds[2:])]; pad = 1000
xmin, ymin, xmax, ymax = xmin - pad, ymin - pad, xmax + pad, ymax + pad
dtm, dw, dh = calculate_default_transform(CRS, "EPSG:3857", int((xmax - xmin) / 20), int((ymax - ymin) / 20),
                                          xmin, ymin, xmax, ymax, resolution=20)
tr = Transformer.from_crs(3857, 4326, always_xy=True)
lo0, la0 = tr.transform(dtm.c, dtm.f + dh * dtm.e); lo1, la1 = tr.transform(dtm.c + dw * dtm.a, dtm.f)
bounds = [[la0, lo0], [la1, lo1]]


def warp_src(path, band=1, resamp=Resampling.bilinear, nodata=0):
    with rasterio.open(path) as s:
        o = np.full((dh, dw), np.nan, np.float32)
        reproject(rasterio.band(s, band), o, dst_transform=dtm, dst_crs="EPSG:3857", resampling=resamp, src_nodata=nodata, dst_nodata=np.nan)
    return o


stats = {}
for date, nm in [("20240622", "s2_20240622"), ("20240707", "s2_20240707")]:
    tci = glob.glob(str(S2 / f"**/*_{date}T*_TCI_20m.jp2"), recursive=True)[0]
    scl = glob.glob(str(S2 / f"**/*_{date}T*_SCL_20m.jp2"), recursive=True)[0]
    rgb = [warp_src(tci, b) for b in (1, 2, 3)]
    a = (~np.isnan(rgb[0])).astype(np.uint8) * 255
    g = lambda x: np.clip(np.nan_to_num(x) * 1.15, 0, 255).astype(np.uint8)
    Image.fromarray(np.dstack([g(rgb[0]), g(rgb[1]), g(rgb[2]), a])).save(OUT / f"{nm}.webp", "WEBP", quality=74, method=6)
    sc = warp_src(scl, resamp=Resampling.nearest)
    stats[f"oblaci_{date}"] = float(np.isin(sc, [3, 8, 9, 10]).sum() / max(1, (~np.isnan(sc)).sum()) * 100)

dn = warp_src(Q / "dNDVI_oranice_bez_zetve.tif", nodata=-9999)
v = np.clip(np.nan_to_num(dn) / 0.4, -1, 1)
red = np.where(v < 0, 215, (1 - v) * 230 + v * 40); grn = np.where(v < 0, (1 + v) * 230 + (-v) * 40, 200 - v * 40)
blu = np.where(v < 0, (1 + v) * 230 + (-v) * 50, (1 - v) * 230 + v * 60)
alpha = np.where(np.isnan(dn) | (dn == 0), 0, np.clip(np.abs(v) * 255 * 1.6, 40, 230))
Image.fromarray(np.dstack([red.astype(np.uint8), grn.astype(np.uint8), blu.astype(np.uint8), alpha.astype(np.uint8)])).save(
    OUT / "dndvi.webp", "WEBP", quality=80, method=6)

# prijave tuče iz ESWD-a (European Severe Weather Database, QC1), 1. 7. 2024. oko 17:10 UTC
eswd = [{"lat": 45.0780, "lon": 18.6980, "promjer_cm": 4.5, "vrijeme": "1. 7. 2024. 17:10 UTC", "qc": "QC1"}]
json.dump({"bounds": bounds, "stats": stats, "eswd": eswd, "eswd_max_cm": 6.5}, open(OUT / "meta.json", "w"))
print("Gotovo:", stats)
