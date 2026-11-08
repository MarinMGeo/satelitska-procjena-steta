# Reprodukcija analize u otvorenom kodu (QGIS) i usporedba s izvornom analizom

Izvorna analiza provedena je u ESA SNAP-u (predobrada Sentinel-1) i ArcGIS Pro. Cijeli postupak zatim je ponovljen
u QGIS-u 3.34 (Processing: GDAL i nativni algoritmi) skriptama `qgis_poplava.py` i `qgis_tuca.py`, s istim ulaznim
podacima i istim pragovima. Rezultati su uspoređeni parcelu po parcelu.

## Poplava (Sentinel-1, 5., 17. i 29. 5. 2023.)

| Korak | ArcGIS Pro | QGIS | Podudaranje |
|---|---|---|---|
| Rasterska detekcija poplave (pikseli 10 m) | 154.210 | 154.210 | identično, piksel po piksel |
| Svi poligoni poplave | 3.678 / 1.542,10 ha | 3.678 / 1.542,10 ha | identično |
| Poligoni ≥ 0,05 ha | 1.528 / 1.502,62 ha | 1.574 / 1.504,92 ha | razlika 46 poligona od točno 5 piksela |
| Poplavljene ARKOD parcele | 3.921 / 844,88 ha | 3.927 / 845,31 ha | 99,97 % parcela u istom razredu |

Jedina razlika je u poligonima od točno pet piksela (0,05 ha). ArcGIS je dijelu njih zbog zaokruživanja izračunao
površinu 0,0499999 ha pa ih je filtar „≥ 0,05 ha” odbacio. QGIS skripta površinu zaokružuje na 1 m², pa ih zadržava
dosljedno. Svi poligoni veći od pet piksela (1.429) potpuno su isti.

## Tuča (Sentinel-2, 22. 6. i 7. 7. 2024.)

| Pokazatelj | ArcGIS Pro (studenti) | QGIS |
|---|---|---|
| Klasa 0 / 1 / 2 / 3 / žetva | 5.232 / 584 / 381 / 22 / 2.184 | 5.184 / 576 / 374 / 21 / 2.248 |
| Parcele u klasama 1–3 | 987 parcela, 1.971 ha | 971 parcela, 1.935 ha |
| Referentna srednja vrijednost i st. devijacija dNDVI | −0,0243 / 0,1851 | −0,0262 / 0,1887 |

- Među parcelama ocijenjenima u obje analize 98,6 % ima istu klasu, a nijedna se ne razlikuje za više od jedne klase.
- Srednji dNDVI po parceli: korelacija 0,994, medijan apsolutne razlike 0,004.
- Razlike potječu od mreže piksela: u ArcGIS-u je snimka od 7. 7. preprojicirana sa zadanom veličinom piksela 10,34 m,
  a QGIS skripta sve radi na mreži od 10 m. Zbog toga se na rubu žetve neke parcele svrstavaju u „žetvu” umjesto u klasu 0
  i obrnuto.
- Pojas tuče: QGIS skripta pojas definira kao skupine od najmanje 50 povezanih piksela ispod praga (1.697 ha).
  Studentski pojas (6.978 ha) šira je zona koja obuhvaća 84 % tih piksela i okolne parcele. Pojas služi samo za prikaz.
  Klase štete ne ovise o njemu.

## Zaključak

Postupak ne ovisi o komercijalnom softveru. Poplava se u QGIS-u reproducira praktički identično, a klase štete od tuče
podudaraju se u 98,6 % ocijenjenih parcela. Brojke u aplikaciji potječu iz izvorne analize.

## Pokretanje

QGIS 3.28 ili noviji (Windows: OSGeo4W Shell; Linux: `python3`):

```
python3 qgis_poplava.py ulaz_poplava izlaz_poplava
python3 qgis_tuca.py <SAFE 22. 6.> <SAFE 7. 7.> jls_tuca.gpkg arkod_2024.gpkg izlaz_tuca
```

Ulazne datoteke opisane su u zaglavlju svake skripte.
