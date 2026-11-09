"""
Tuča, Gradište, Županja i Štitar (1. 7. 2024.): pojas tuče i klase štete po ARKOD oranicama iz Sentinel-2,
u QGIS-u (Processing: GDAL i nativni algoritmi; NumPy za filtar većine). Licencija: EUPL-1.2

Ulaz:
  <safe_prije>   Sentinel-2 L2A SAFE, 22. 6. 2024. (T33TYL)
  <safe_poslije> Sentinel-2 L2A SAFE, 7. 7. 2024. (T33TYL)
  <jls>          granice JLS (DGU): Gradište, Županja, Štitar
  <arkod>        ARKOD parcele 2024. (APPRRR); koriste se oranice (land_use_i = 200)

Pokretanje (QGIS 3.28 ili noviji):
  python3 qgis_tuca.py <safe_prije> <safe_poslije> <jls> <arkod> <izlaz> [unutarnji_pojas_m]
  (Linux, ili OSGeo4W Shell na Windowsima; u QGIS Python konzoli pozvati main(...))

Koraci (isti kao u izvornoj analizi):
  1. Područje: JLS + pojas od 5 km. Mreža 10 m u HTRS96/TM.
  2. Za oba datuma: refleksija (DN - 1000) / 10000, kanali od 20 m bilinearno na 10 m, maska SCL (samo 4 vegetacija
     i 5 golo tlo) i šest indeksa: NDVI (B08, B04; NDVI > 1 se odbacuje), NDRE (B8A, B05), NDMI (B08, B11),
     PSRI ((B04 - B02) / B06), MSAVI2 (B08, B04) i BSI ((B11 + B04) - (B08 + B02)) / ((B11 + B04) + (B08 + B02)).
  3. dNDVI = NDVI(7. 7.) - NDVI(22. 6.).
  4. Maska žetve: NDVI(22. 6.) < 0,4  ili  (NDVI(7. 7.) < 0,25 i BSI(7. 7.) > 0,1). Ti pikseli se ne ocjenjuju.
  5. Oranice suzene za 10 m (rubni pikseli), dNDVI samo unutar njih.
  6. Pojas tuče: dNDVI <= -0,05, filtar većine 3 x 3 (8 susjeda), skupine povezanih piksela (8 susjeda), odbacivanje
     skupina manjih od 50 piksela, pretvorba u poligone.
  7. Zonalna statistika po parceli (srednja vrijednost, st. devijacija, broj piksela dNDVI; udio piksela ispod praga;
     srednja vrijednost svakog indeksa prije i poslije).
  8. z = (MEAN - srednja vrijednost svih ocijenjenih parcela) / st. devijacija; klase 1, 2, 3 za z <= -1, -2, -3.
     Parcele bez ijednog valjanog piksela: "nije ocijenjeno - žetva".
"""
import os, sys, glob, pathlib
import numpy as np

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from qgis.core import (QgsApplication, QgsVectorLayer, QgsRasterLayer, QgsCoordinateReferenceSystem, QgsRectangle,
                       QgsField, edit)
from qgis.PyQt.QtCore import QVariant

PRAG_TUCA, MIN_PIKSELA, PIKSEL = -0.05, 50, 10.0
MASKA_ZETVE = "(A < 0.4) | ((B < 0.25) & (C > 0.1))"   # A = NDVI prije, B = NDVI poslije, C = BSI poslije
ND = -9999.0


def start_qgis():
    if QgsApplication.instance() is not None:
        import processing
        return None, processing
    QgsApplication.setPrefixPath(os.environ.get("QGIS_PREFIX_PATH", "/usr"), True)
    app = QgsApplication([], False); app.initQgis()
    for p in ["/usr/share/qgis/python/plugins", os.path.join(os.environ.get("QGIS_PREFIX_PATH", ""), "python", "plugins")]:
        if os.path.isdir(p): sys.path.append(p)
    import processing
    from processing.core.Processing import Processing
    from qgis.analysis import QgsNativeAlgorithms
    Processing.initialize()
    QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
    return app, processing


def kanal(safe, ime):
    """Putanja do kanala u SAFE mapi (10 m ako postoji, inače 20 m)."""
    for r in ("10m", "20m"):
        f = glob.glob(str(pathlib.Path(safe) / "**" / f"*_{ime}_{r}.jp2"), recursive=True)
        if f: return f[0]
    raise FileNotFoundError(f"{ime} u {safe}")


def main(safe_prije, safe_poslije, jls, arkod, izlaz, unutarnji_pojas=-10.0):
    izlaz = pathlib.Path(izlaz).resolve(); izlaz.mkdir(parents=True, exist_ok=True)
    app, processing = start_qgis()
    from osgeo import gdal
    run = lambda alg, **p: processing.run(alg, p)
    tmp = lambda n: str(izlaz / n)
    crs = QgsCoordinateReferenceSystem("EPSG:3765")

    # 1. područje i mreža (obuhvat pojasa od 5 km poravnat na 10 m)
    pojas5 = run("native:buffer", INPUT=str(jls), DISTANCE=5000, SEGMENTS=16, DISSOLVE=True,
                 OUTPUT=tmp("podrucje_5km.gpkg"))["OUTPUT"]
    e = QgsVectorLayer(pojas5, "p").extent()
    sn = lambda v, f: f(v / PIKSEL) * PIKSEL
    mreza = QgsRectangle(sn(e.xMinimum(), np.floor), sn(e.yMinimum(), np.floor), sn(e.xMaximum(), np.ceil), sn(e.yMaximum(), np.ceil))

    def na_mrezu(src, ime, resampling):
        return run("gdal:warpreproject", INPUT=src, TARGET_CRS=crs, RESAMPLING=resampling, NODATA=0,
                   TARGET_RESOLUTION=PIKSEL, TARGET_EXTENT=mreza, TARGET_EXTENT_CRS=crs, DATA_TYPE=0,
                   OUTPUT=tmp(ime))["OUTPUT"]

    def calc(ime, formula, **ulazi):
        p = dict(FORMULA=formula, NO_DATA=ND, RTYPE=5, OUTPUT=tmp(ime))
        for k, v in ulazi.items(): p[f"INPUT_{k}"] = v; p[f"BAND_{k}"] = 1
        return run("gdal:rastercalculator", **p)["OUTPUT"]

    # 2. indeksi za oba datuma (refleksija, maska SCL: samo 4 vegetacija i 5 golo tlo)
    I, IX = {}, {}
    for kad, safe in (("prije", safe_prije), ("poslije", safe_poslije)):
        b = {k: na_mrezu(kanal(safe, k), f"{kad}_{k}.tif", 0 if k in ("B02", "B04", "B08") else 1)
             for k in ("B02", "B04", "B05", "B06", "B08", "B8A", "B11")}
        scl = na_mrezu(kanal(safe, "SCL"), f"{kad}_SCL.tif", 0)
        r = lambda X: f"(({X} - 1000.0) / 10000.0)"
        ok = lambda *xs: "((E == 4) | (E == 5))" + "".join(f" & ({x} > 0)" for x in xs)
        nd = lambda a, b_: f"({r(a)} - {r(b_)}) / ({r(a)} + {r(b_)})"
        ndvi = calc(f"NDVI_{kad}.tif", f"where({ok('A', 'B')}, where({nd('B', 'A')} <= 1, {nd('B', 'A')}, {ND}), {ND})",
                    A=b["B04"], B=b["B08"], E=scl)
        bsi = calc(f"BSI_{kad}.tif",
                   f"where({ok('A', 'B', 'C', 'D')}, (({r('C')} + {r('A')}) - ({r('B')} + {r('D')})) / (({r('C')} + {r('A')}) + ({r('B')} + {r('D')})), {ND})",
                   A=b["B04"], B=b["B08"], C=b["B11"], D=b["B02"], E=scl)
        ndre = calc(f"NDRE_{kad}.tif", f"where({ok('A', 'B')}, {nd('A', 'B')}, {ND})", A=b["B8A"], B=b["B05"], E=scl)
        ndmi = calc(f"NDMI_{kad}.tif", f"where({ok('A', 'B')}, {nd('A', 'B')}, {ND})", A=b["B08"], B=b["B11"], E=scl)
        psri = calc(f"PSRI_{kad}.tif", f"where({ok('A', 'B', 'C')}, ({r('A')} - {r('B')}) / {r('C')}, {ND})",
                    A=b["B04"], B=b["B02"], C=b["B06"], E=scl)
        msavi = calc(f"MSAVI2_{kad}.tif",
                     f"where({ok('A', 'B')}, (2 * {r('B')} + 1 - sqrt(maximum((2 * {r('B')} + 1) ** 2 - 8 * ({r('B')} - {r('A')}), 0))) / 2, {ND})",
                     A=b["B04"], B=b["B08"], E=scl)
        I[kad] = (ndvi, bsi)
        IX.update({f"NDVI_{kad}": ndvi, f"NDRE_{kad}": ndre, f"NDMI_{kad}": ndmi, f"MSAVI2_{kad}": msavi, f"PSRI_{kad}": psri, f"BSI_{kad}": bsi})

    # 3.-4. dNDVI bez žetve
    v = lambda X: f"({X} > -9000)"
    dndvi = calc("dNDVI.tif", f"where({v('A')} & {v('B')}, B - A, {ND})", A=I["prije"][0], B=I["poslije"][0])
    zetva = calc("maska_zetve.tif", f"where({v('A')} & {v('B')} & {v('C')}, {MASKA_ZETVE}, 0)",
                 A=I["prije"][0], B=I["poslije"][0], C=I["poslije"][1])

    # 5. oranice, unutarnji pojas, raster maska oranica
    oranice = run("native:extractbyexpression", INPUT=str(arkod), EXPRESSION='"land_use_i" = 200', OUTPUT="TEMPORARY_OUTPUT")["OUTPUT"]
    oranice = run("native:extractbylocation", INPUT=oranice, PREDICATE=[0], INTERSECT=pojas5, OUTPUT="TEMPORARY_OUTPUT")["OUTPUT"]
    if unutarnji_pojas:
        oranice = run("native:buffer", INPUT=oranice, DISTANCE=unutarnji_pojas, SEGMENTS=8, DISSOLVE=False, OUTPUT="TEMPORARY_OUTPUT")["OUTPUT"]
    oranice = run("native:savefeatures", INPUT=oranice, OUTPUT=tmp("oranice_unutarnji_pojas.gpkg"))["OUTPUT"]
    maska_or = run("gdal:rasterize", INPUT=oranice, BURN=1, UNITS=1, WIDTH=PIKSEL, HEIGHT=PIKSEL, EXTENT=mreza,
                   NODATA=0, DATA_TYPE=0, INIT=0, OUTPUT=tmp("maska_oranica.tif"))["OUTPUT"]
    dnd_or = calc("dNDVI_oranice_bez_zetve.tif", f"where((B == 1) & {v('A')} & (C == 0), A, {ND})", A=dndvi, B=maska_or, C=zetva)
    prag = calc("tuca_prag.tif", f"where({v('A')}, A <= {PRAG_TUCA}, {ND})", A=dnd_or)

    # 6. pojas tuče: filtar većine 3 x 3, povezane skupine >= 50 piksela, poligoni
    ds = gdal.Open(prag); a = ds.GetRasterBand(1).ReadAsArray(); valid = a > -9000; t = (a == 1)
    pad = lambda x: np.pad(x, 1)
    T, V = pad(t).astype(np.int8), pad(valid).astype(np.int8)
    jed = sum(np.roll(np.roll(T, dy, 0), dx, 1) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dy or dx)[1:-1, 1:-1]
    nul = sum(np.roll(np.roll(V - T, dy, 0), dx, 1) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dy or dx)[1:-1, 1:-1]
    maj = np.where(jed >= 5, 1, np.where(nul >= 5, 0, t.astype(np.int8)))   # MAJORITY: većina od 8 susjeda
    maj = np.where(valid, maj, 255).astype(np.uint8)
    drv = gdal.GetDriverByName("GTiff"); o = drv.Create(tmp("tuca_vecina.tif"), ds.RasterXSize, ds.RasterYSize, 1, gdal.GDT_Byte, ["COMPRESS=DEFLATE"])
    o.SetGeoTransform(ds.GetGeoTransform()); o.SetProjection(ds.GetProjection()); o.GetRasterBand(1).SetNoDataValue(255)
    o.GetRasterBand(1).WriteArray(maj); o = None; ds = None
    pol = run("gdal:polygonize", INPUT=tmp("tuca_vecina.tif"), BAND=1, FIELD="DN", EIGHT_CONNECTEDNESS=True,
              OUTPUT=tmp("tuca_poligoni_svi.gpkg"))["OUTPUT"]
    pojas = run("native:extractbyexpression", INPUT=pol, EXPRESSION=f'"DN" = 1 AND round(area($geometry)) >= {MIN_PIKSELA * PIKSEL * PIKSEL}',
                OUTPUT=tmp("pojas_tuce.gpkg"))["OUTPUT"]

    # 7. zonalna statistika po parceli
    par = run("native:zonalstatisticsfb", INPUT=oranice, INPUT_RASTER=dnd_or, RASTER_BAND=1, COLUMN_PREFIX="dNDVI_",
              STATISTICS=[0, 2, 4], OUTPUT="TEMPORARY_OUTPUT")["OUTPUT"]           # count, mean, std
    par = run("native:zonalstatisticsfb", INPUT=par, INPUT_RASTER=prag, RASTER_BAND=1, COLUMN_PREFIX="udio_",
              STATISTICS=[2], OUTPUT="TEMPORARY_OUTPUT")["OUTPUT"]                 # udio piksela ispod praga
    for ime, ras in IX.items():                                                     # srednja vrijednost svakog indeksa
        par = run("native:zonalstatisticsfb", INPUT=par, INPUT_RASTER=ras, RASTER_BAND=1, COLUMN_PREFIX=f"{ime}_",
                  STATISTICS=[2], OUTPUT="TEMPORARY_OUTPUT")["OUTPUT"]
    par = run("native:savefeatures", INPUT=par, OUTPUT=tmp("oranice_statistika.gpkg"))["OUTPUT"]

    # 8. z-vrijednost i klase
    L = QgsVectorLayer(par, "p")
    mean = np.array([f["dNDVI_mean"] if f["dNDVI_count"] else np.nan for f in L.getFeatures()], float)
    ok = ~np.isnan(mean); mu, sd = float(mean[ok].mean()), float(mean[ok].std())
    print(f"referenca (sve ocijenjene oranice, n = {ok.sum()}): srednja vrijednost {mu:.6f}, st. devijacija {sd:.6f}")
    with edit(L):
        L.addAttribute(QgsField("z", QVariant.Double)); L.addAttribute(QgsField("klasa", QVariant.Int))
        L.addAttribute(QgsField("klasa_stete", QVariant.String)); L.updateFields()
        iz, ik, it = (L.fields().indexOf(n) for n in ("z", "klasa", "klasa_stete"))
        for f, m in zip(L.getFeatures(), mean):
            if np.isnan(m): z, k, txt = None, -1, "nije ocijenjeno – žetva"
            else:
                z = float((m - mu) / sd); k = 3 if z <= -3 else 2 if z <= -2 else 1 if z <= -1 else 0
                txt = ["Klasa 0 – bez izdvojenog pada", "Klasa 1 – moguća šteta", "Klasa 2 – vjerojatna šteta", "Klasa 3 – jaka šteta"][k]
            L.changeAttributeValues(f.id(), {iz: z, ik: k, it: txt})
    run("native:savefeatures", INPUT=L, OUTPUT=tmp("ARKOD_oranice_klase_stete.gpkg"))
    kl = [f["klasa"] for f in L.getFeatures()]
    print("Gotovo: " + ", ".join(f"{n}: {kl.count(k)}" for k, n in ((0, "klasa 0"), (1, "klasa 1"), (2, "klasa 2"), (3, "klasa 3"), (-1, "žetva")))
          + f"; pojas tuče {sum(f.geometry().area() for f in QgsVectorLayer(pojas, 'x').getFeatures()) / 1e4:.0f} ha")
    if app: app.exitQgis()


if __name__ == "__main__":
    a = sys.argv[1:]
    main(*a[:5], *(float(x) for x in a[5:6]))
