"""Zajedničke funkcije za čitanje rezultata obrade u QGIS-u (EUPL-1.2)."""
import pathlib
import numpy as np, pyogrio


def read_tif(path, nodata_values=(-9999, 255)):
    """GeoTIFF iz QGIS obrade -> (polje float32 s NaN, transformacija)."""
    import rasterio
    with rasterio.open(path) as r:
        a = r.read(1).astype(np.float32); nd = r.nodata
    for v in ([nd] if nd is not None else []) + list(nodata_values):
        a[a == v] = np.nan
    return a, r.transform


def qgis_poplava(ulaz, izlaz):
    """Rezultati qgis_poplava.py: detekcija, VV u dB (5., 17., 29. 5.), parcele s poplavom i poligoni poplave."""
    ulaz, izlaz = pathlib.Path(ulaz), pathlib.Path(izlaz)
    det, dt = read_tif(izlaz / "S1A_VV_17052023_poplava_detekcija.tif")
    vv = {d: read_tif(ulaz / f"S1A_VV_{d}052023_dB.tif") for d in ("05", "17", "29")}
    par = pyogrio.read_dataframe(izlaz / "ARKOD_2024_poplava.gpkg")
    par["fha"] = par.poplava_ha.fillna(0)
    return det, dt, vv, par
