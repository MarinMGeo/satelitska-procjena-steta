"""
Poplava Kupe i Korane (svibanj 2023.): detekcija poplave iz Sentinel-1 i presjek s ARKOD parcelama,
u cijelosti u QGIS-u (Processing: GDAL i nativni algoritmi). Licencija: EUPL-1.2

Ulaz (mapa <ulaz>):
  S1A_VV_05052023_dB.tif, S1A_VV_17052023_dB.tif, S1A_VV_29052023_dB.tif   (ili *_sigma0.tif u linearnim jedinicama)
      Sentinel-1 GRD, polarizacija VV, obrađeno u ESA SNAP-u (Apply Orbit File, Thermal Noise Removal,
      Calibration -> Sigma0, Speckle Filter, Range-Doppler Terrain Correction, 10 m, HTRS96/TM) i izrezano na
      područje istraživanja. Ako su snimke u linearnim jedinicama (*_sigma0.tif), skripta ih pretvara u dB: 10 * log10(sigma0).
  jls_podrucje.gpkg   granice JLS (DGU): Karlovac, Duga Resa, Barilović, Lasinja
  arkod_2024.gpkg     ARKOD parcele 2024. (APPRRR)

Pokretanje (QGIS 3.28 ili noviji):
  python3 qgis_poplava.py <ulaz> <izlaz>          (Linux, ili OSGeo4W Shell na Windowsima)
  ili u QGIS-u: Plugins -> Python Console -> Show Editor -> otvoriti skriptu, prilagoditi ULAZ/IZLAZ i Run.

Koraci (isti kao u izvornoj analizi):
  1. Područje istraživanja: JLS + pojas od 3 km; ARKOD parcele koje ga dodiruju.
  2. Sva tri datuma na zajedničku mrežu (najbliži susjed, 10 m).
  3. Vremenska detekcija promjene. Piksel je poplavljen ako vrijedi:
       VV(17. 5.) < -16 dB  i  VV(17. 5.) - VV(5. 5.) < -3 dB  i  VV(29. 5.) - VV(17. 5.) > +3 dB
  4. Rasterska maska u poligone (4-susjedstvo), površina u ha, uklanjanje poligona < 0,05 ha.
  5. Presjek s ARKOD-om, zbroj poplavljene površine po parceli, postotak i razred poplavljenosti
     (0: 0 %, 1: do 25 %, 2: 25-50 %, 3: 50-75 %, 4: više od 75 %).
"""
import os, sys, pathlib

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from qgis.core import QgsApplication, QgsVectorLayer, QgsRasterLayer, QgsCoordinateReferenceSystem, QgsRectangle

PRAG_VV17, PRAG_PAD, PRAG_POVRAT, MIN_HA, POJAS_M, PIKSEL = -16.0, -3.0, 3.0, 0.05, 3000, 10.0


def start_qgis():
    if QgsApplication.instance() is not None:  # pokrenuto iz QGIS konzole
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


def main(ulaz, izlaz):
    ulaz, izlaz = pathlib.Path(ulaz).resolve(), pathlib.Path(izlaz).resolve(); izlaz.mkdir(parents=True, exist_ok=True)
    app, processing = start_qgis()
    run = lambda alg, **p: processing.run(alg, p)
    tmp = lambda n: str(izlaz / n)

    # 1. područje istraživanja
    pojas = run("native:buffer", INPUT=str(ulaz / "jls_podrucje.gpkg"), DISTANCE=POJAS_M, SEGMENTS=16,
                DISSOLVE=True, OUTPUT=tmp("podrucje_istrazivanja_3km.gpkg"))["OUTPUT"]
    arkod = run("native:extractbylocation", INPUT=str(ulaz / "arkod_2024.gpkg"), PREDICATE=[0],
                INTERSECT=pojas, OUTPUT="TEMPORARY_OUTPUT")["OUTPUT"]
    arkod = run("native:fieldcalculator", INPUT=arkod, FIELD_NAME="ARKOD_ha", FIELD_TYPE=0, FIELD_LENGTH=20,
                FIELD_PRECISION=6, FORMULA="area($geometry) / 10000", OUTPUT="TEMPORARY_OUTPUT")["OUTPUT"]

    # 2. rasteri promjene. Snimke nisu na istoj mreži (pomak do pola piksela), pa se svaki izračun radi
    #    na mreži presjeka ulaznih rastera (najbliži susjed), istim pravilom kao u izvornoj analizi.
    def db(d):
        f = ulaz / f"S1A_VV_{d}052023_dB.tif"
        if f.exists(): return str(f)
        return run("gdal:rastercalculator", INPUT_A=str(ulaz / f"S1A_VV_{d}052023_sigma0.tif"), BAND_A=1, RTYPE=5, NO_DATA=-9999,
                   FORMULA="where(A > 0, 10 * log10(A), -9999)", OUTPUT=tmp(f"S1A_VV_{d}052023_dB.tif"))["OUTPUT"]

    R = {d: QgsRasterLayer(db(d), d) for d in ("05", "17", "29")}
    crs = QgsCoordinateReferenceSystem("EPSG:3765")

    def na_mrezu(src, ref, ime):  # ref: raster (njegova mreža) ili QgsRectangle
        ex = ref if isinstance(ref, QgsRectangle) else QgsRasterLayer(ref, "ref").extent()
        return run("gdal:warpreproject", INPUT=src, TARGET_CRS=crs, RESAMPLING=0, NODATA=-9999,
                   TARGET_RESOLUTION=PIKSEL, TARGET_EXTENT=ex, TARGET_EXTENT_CRS=crs,
                   DATA_TYPE=6, OUTPUT=tmp(ime))["OUTPUT"]

    def presjek(*rasteri):
        """Presjek obuhvata rastera, ishodište u donjem lijevom kutu, cijeli pikseli."""
        E = [QgsRasterLayer(x, "e").extent() for x in rasteri]
        x0 = max(e.xMinimum() for e in E); y0 = max(e.yMinimum() for e in E)
        nx = round((min(e.xMaximum() for e in E) - x0) / PIKSEL); ny = round((min(e.yMaximum() for e in E) - y0) / PIKSEL)
        return QgsRectangle(x0, y0, x0 + nx * PIKSEL, y0 + ny * PIKSEL)

    def razlika(a, b, ime):  # a - b na mreži presjeka
        m = presjek(a, b)
        aw, bw = na_mrezu(a, m, "_a_" + ime), na_mrezu(b, m, "_b_" + ime)
        return run("gdal:rastercalculator", INPUT_A=aw, BAND_A=1, INPUT_B=bw, BAND_B=1, NO_DATA=-9999, RTYPE=5,
                   FORMULA="where((A > -9000) & (B > -9000), A - B, -9999)", OUTPUT=tmp(ime))["OUTPUT"]

    v05, v17, v29 = (R[d].source() for d in ("05", "17", "29"))
    pad = razlika(v17, v05, "S1A_razlika_VV_17_05.tif")      # VV(17. 5.) - VV(5. 5.)
    povrat = razlika(v29, v17, "S1A_razlika_VV_29_17.tif")   # VV(29. 5.) - VV(17. 5.)

    # 3. vremenska detekcija promjene (1 = poplava, 0 = nije, 255 = izvan snimke) na mreži presjeka ulaza
    mreza = presjek(v17, pad, povrat)
    a = na_mrezu(v17, mreza, "VV_17_mreza.tif"); b = na_mrezu(pad, mreza, "razlika_17_05_mreza.tif")
    c = na_mrezu(povrat, mreza, "razlika_29_17_mreza.tif")
    formula = (f"where((A > -9000) & (B > -9000) & (C > -9000), "
               f"(A < {PRAG_VV17}) * (B < {PRAG_PAD}) * (C > {PRAG_POVRAT}), 255)")
    det = run("gdal:rastercalculator", INPUT_A=a, BAND_A=1, INPUT_B=b, BAND_B=1, INPUT_C=c, BAND_C=1,
              FORMULA=formula, NO_DATA=255, RTYPE=0, OUTPUT=tmp("S1A_VV_17052023_poplava_detekcija.tif"))["OUTPUT"]

    # 4. poligoni poplave >= 0,05 ha
    pol = run("gdal:polygonize", INPUT=det, BAND=1, FIELD="DN", EIGHT_CONNECTEDNESS=False,
              OUTPUT=tmp("poplava_poligoni_svi.gpkg"))["OUTPUT"]
    pol = run("native:extractbyattribute", INPUT=pol, FIELD="DN", OPERATOR=0, VALUE="1", OUTPUT="TEMPORARY_OUTPUT")["OUTPUT"]
    # površina zaokružena na 1 m2, da poligon od točno 5 piksela (0,05 ha) ne ispadne zbog pogreške zaokruživanja
    pol = run("native:fieldcalculator", INPUT=pol, FIELD_NAME="povrsina_ha", FIELD_TYPE=0, FIELD_LENGTH=20, FIELD_PRECISION=6,
              FORMULA="round(area($geometry)) / 10000", OUTPUT="TEMPORARY_OUTPUT")["OUTPUT"]
    pol = run("native:extractbyexpression", INPUT=pol, EXPRESSION=f'"povrsina_ha" >= {MIN_HA}',
              OUTPUT=tmp("poplava_poligoni_005ha.gpkg"))["OUTPUT"]

    # 5. presjek s ARKOD-om i razredi po parceli
    pres = run("native:intersection", INPUT=arkod, OVERLAY=pol, INPUT_FIELDS=["id"], OVERLAY_FIELDS=["povrsina_ha"],
               OUTPUT="TEMPORARY_OUTPUT")["OUTPUT"]
    pres = run("native:fieldcalculator", INPUT=pres, FIELD_NAME="poplava_ha", FIELD_TYPE=0, FIELD_LENGTH=20, FIELD_PRECISION=6,
               FORMULA="area($geometry) / 10000", OUTPUT="TEMPORARY_OUTPUT")["OUTPUT"]
    zbroj = run("qgis:statisticsbycategories", INPUT=pres, VALUES_FIELD_NAME="poplava_ha", CATEGORIES_FIELD_NAME=["id"],
                OUTPUT="TEMPORARY_OUTPUT")["OUTPUT"]
    par = run("native:joinattributestable", INPUT=arkod, FIELD="id", INPUT_2=zbroj, FIELD_2="id", FIELDS_TO_COPY=["sum"],
              METHOD=1, PREFIX="poplava_", OUTPUT="TEMPORARY_OUTPUT")["OUTPUT"]
    par = run("native:fieldcalculator", INPUT=par, FIELD_NAME="poplava_ha", FIELD_TYPE=0, FIELD_LENGTH=20, FIELD_PRECISION=6,
              FORMULA='coalesce("poplava_sum", 0)', OUTPUT="TEMPORARY_OUTPUT")["OUTPUT"]
    par = run("native:fieldcalculator", INPUT=par, FIELD_NAME="posto_poplavljenosti", FIELD_TYPE=0, FIELD_LENGTH=10, FIELD_PRECISION=2,
              FORMULA='round(100 * "poplava_ha" / "ARKOD_ha", 2)', OUTPUT="TEMPORARY_OUTPUT")["OUTPUT"]
    par = run("native:fieldcalculator", INPUT=par, FIELD_NAME="razred_poplavljenosti", FIELD_TYPE=1, FIELD_LENGTH=2, FIELD_PRECISION=0,
              FORMULA='CASE WHEN "posto_poplavljenosti" <= 0 THEN 0 WHEN "posto_poplavljenosti" <= 25 THEN 1 '
                      'WHEN "posto_poplavljenosti" <= 50 THEN 2 WHEN "posto_poplavljenosti" <= 75 THEN 3 ELSE 4 END',
              OUTPUT=tmp("ARKOD_2024_poplava.gpkg"))["OUTPUT"]

    v = QgsVectorLayer(par, "p"); n = sum(1 for f in v.getFeatures() if f["poplava_ha"] > 0)
    ha = sum(f["poplava_ha"] for f in v.getFeatures())
    print(f"Gotovo: {QgsVectorLayer(pol, 'x').featureCount()} poligona poplave, {n} poplavljenih parcela, {ha:.2f} ha na parcelama")
    if app: app.exitQgis()


if __name__ == "__main__":
    main(*(sys.argv[1:3] if len(sys.argv) > 2 else ("ulaz_poplava", "izlaz_poplava")))
