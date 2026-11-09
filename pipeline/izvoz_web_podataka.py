"""
Izvoz rezultata analize poplave iz QGIS-a (qgis_poplava.py) u lagane web formate za aplikaciju u mapi docs/.

Pokretanje:
    pip install geopandas pyogrio rasterio pillow pyproj numpy
    python izvoz_web_podataka.py <ulaz_poplava> <izlaz_poplava> ../docs/data

<ulaz_poplava>: S1A_VV_{05,17,29}052023_dB.tif (ESA SNAP), jls_podrucje.gpkg (DGU), vodotoci.gpkg (Hrvatske vode)
<izlaz_poplava>: ARKOD_2024_poplava.gpkg i poplava_poligoni_005ha.gpkg iz qgis_poplava.py

Licencija: EUPL-1.2
"""
import json, sys, pathlib
import numpy as np, pyogrio, geopandas as gpd
import rasterio
from rasterio.warp import reproject, Resampling, calculate_default_transform
from PIL import Image
from pyproj import Transformer

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from izvoz_web_podataka_lib import qgis_poplava  # noqa: E402

ULAZ, QOUT, OUT = map(pathlib.Path, sys.argv[1:4]); OUT.mkdir(parents=True, exist_ok=True)
SRC_CRS = "EPSG:3765"  # HTRS96/TM


def enc_geom(geom, scale=1e5):
    """Kompaktni zapis poligona: cjelobrojne koordinate (1e-5 °) s delta kodiranjem."""
    out = []
    for pg in ([geom] if geom.geom_type == "Polygon" else geom.geoms):
        rings = []
        for ring in [pg.exterior, *pg.interiors]:
            c = np.round(np.asarray(ring.coords)[:-1] * scale).astype(np.int64)
            if len(c) >= 3:
                rings.append(np.vstack([c[:1], np.diff(c, axis=0)]).ravel().tolist())
        if rings: out.append(rings)
    return out


# ---------- vektori ----------
_, _, VV, par = qgis_poplava(ULAZ, QOUT)
jls = pyogrio.read_dataframe(ULAZ / "jls_podrucje.gpkg")[["JLS_IME_HR", "geometry"]]
pts = par[["id", "geometry"]].copy(); pts["geometry"] = par.geometry.representative_point()
jmap = gpd.sjoin(pts, jls, how="left", predicate="within").index_right.fillna(-1).astype(int)

par["geometry"] = par.geometry.simplify(1.5, preserve_topology=True)
par = par.to_crs(4326)
props, geoms = [], []
for i, r in par.iterrows():
    f = r.fha > 0
    props.append([int(r.id), int(r.land_use_i), round(r.ARKOD_ha, 4), round(r.fha, 4) if f else 0,
                  round(r.posto_poplavljenosti or 0, 1) if f else 0, int(r.razred_poplavljenosti) if f else 0,
                  r.home_name or "", int(jmap.loc[i])])
    geoms.append(enc_geom(r.geometry))
json.dump({"fields": ["id", "lu", "ha", "fha", "pct", "r", "toponim", "j"], "scale": 1e5,
           "jls": jls.JLS_IME_HR.tolist(), "props": props, "geoms": geoms},
          open(OUT / "parcele.json", "w"), separators=(",", ":"))

pop = pyogrio.read_dataframe(QOUT / "poplava_poligoni_005ha.gpkg")
pop["geometry"] = pop.geometry.simplify(2, preserve_topology=True); pop = pop.to_crs(4326)
json.dump({"scale": 1e5, "props": [[round(x, 3)] for x in pop.povrsina_ha], "geoms": [enc_geom(g) for g in pop.geometry]},
          open(OUT / "poplava.json", "w"), separators=(",", ":"))

j4 = jls.to_crs(4326); j4["geometry"] = j4.geometry.simplify(0.0002)
j4.to_file(OUT / "jls.geojson", driver="GeoJSON", COORDINATE_PRECISION=5)
riv = pyogrio.read_dataframe(ULAZ / "vodotoci.gpkg").to_crs(4326); riv["geometry"] = riv.geometry.simplify(0.0001)
riv[["geometry"]].to_file(OUT / "rijeke.geojson", driver="GeoJSON", COORDINATE_PRECISION=5)

# ---------- rasteri Sentinel-1 ----------
R = {"v05": VV["05"], "v17": VV["17"], "v29": VV["29"]}
ref, rt = R["v17"]; H, W = ref.shape
left, top = rt.c, rt.f; right, bottom = left + W * rt.a, top + H * rt.e


def warp(k, res):
    a, t = R[k]
    dt, dw, dh = calculate_default_transform(SRC_CRS, "EPSG:3857", W, H, left, bottom, right, top, resolution=res)
    d = np.full((dh, dw), np.nan, np.float32)
    reproject(a, d, src_transform=t, src_crs=SRC_CRS, dst_transform=dt, dst_crs="EPSG:3857",
              resampling=Resampling.average, src_nodata=np.nan, dst_nodata=np.nan)
    return d, dt, dw, dh


def bounds(dt, dw, dh):
    tr = Transformer.from_crs(3857, 4326, always_xy=True)
    lo0, la0 = tr.transform(dt.c, dt.f + dh * dt.e); lo1, la1 = tr.transform(dt.c + dw * dt.a, dt.f)
    return [[la0, lo0], [la1, lo1]]


st = lambda a, lo=-22, hi=-2: (np.clip((a - lo) / (hi - lo), 0, 1) * 255).astype(np.uint8)
# prikazne podloge, 25 m
v5, dt, dw, dh = warp("v05", 25); v17 = warp("v17", 25)[0]; v29 = warp("v29", 25)[0]
alpha = ((~np.isnan(v5) & ~np.isnan(v17)) * 255).astype(np.uint8)
Image.fromarray(np.dstack([st(v5), st(v17), st(v17), alpha])).save(OUT / "sar_rgb.webp", "WEBP", quality=72, method=6)
for k, a in [("0505", v5), ("1705", v17), ("2905", v29)]:
    Image.fromarray(np.dstack([st(a), alpha])).save(OUT / f"sar_{k}.webp", "WEBP", quality=72, method=6)
meta = {"bounds": bounds(dt, dw, dh)}

# podatkovna tekstura za alat praga i radarski potpis, 40 m: R=VV17, G=VV17-VV05, B=VV29-VV17
v5, dt, dw, dh = warp("v05", 40); v17 = warp("v17", 40)[0]; v29 = warp("v29", 40)[0]
q = lambda a, lo, hi: np.clip(np.round((a - lo) / (hi - lo) * 254) + 1, 1, 255)
m = ~np.isnan(v5) & ~np.isnan(v17) & ~np.isnan(v29)
tex = np.dstack([np.where(m, q(v17, -30, 0), 0), np.where(m, q(v17 - v5, -15, 15), 0),
                 np.where(m, q(v29 - v17, -15, 15), 0), m * 255]).astype(np.uint8)
Image.fromarray(tex).save(OUT / "sar_data.png", optimize=True)
meta.update(w=dw, h=dh, res=40, data_bounds=bounds(dt, dw, dh))
json.dump(meta, open(OUT / "raster_meta.json", "w"))
print("Gotovo:", sorted(p.name for p in OUT.iterdir()))
