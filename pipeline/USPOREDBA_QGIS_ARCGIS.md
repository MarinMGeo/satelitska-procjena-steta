# Provjera obrade: QGIS (konačna obrada) i probna obrada u ArcGIS Pro

Sva obrada za aplikaciju provedena je u softveru otvorenog koda: predobrada radarskih snimaka Sentinel-1 u ESA SNAP-u,
a analiza u QGIS-u 3.34 (Processing: GDAL i nativni algoritmi) skriptama `qgis_poplava.py` i `qgis_tuca.py`.
Postupak je prethodno razvijen i testiran u ArcGIS Pro. Usporedba parcelu po parcelu pokazuje da obje obrade daju
praktički iste rezultate, pa rezultat ne ovisi o izboru softvera.

## Poplava (Sentinel-1, 5., 17. i 29. 5. 2023.)

| Korak | QGIS (u aplikaciji) | ArcGIS Pro (test) | Podudaranje |
|---|---|---|---|
| Rasterska detekcija poplave (pikseli 10 m) | 154.210 | 154.210 | identično, piksel po piksel |
| Svi poligoni poplave | 3.678 / 1.542,10 ha | 3.678 / 1.542,10 ha | identično |
| Poligoni ≥ 0,05 ha | 1.574 / 1.504,92 ha | 1.528 / 1.502,62 ha | razlika 46 poligona od točno 5 piksela |
| Poplavljene ARKOD parcele | 3.927 / 845,31 ha | 3.921 / 844,88 ha | 99,97 % parcela u istom razredu |

Jedina razlika su poligoni od točno pet piksela (0,05 ha). U testnoj obradi dio njih je zbog zaokruživanja dobio površinu
0,0499999 ha i ispao iz filtra „≥ 0,05 ha”; QGIS skripta površinu zaokružuje na 1 m² i zadržava ih dosljedno.
Aplikacija prikazuje 3.901 parcelu, jer izostavlja presjeke manje od 0,5 m².

## Tuča (Sentinel-2, 22. 6. i 7. 7. 2024.)

| Pokazatelj | QGIS (u aplikaciji) | ArcGIS Pro (test) |
|---|---|---|
| Klasa 0 / 1 / 2 / 3 / žetva | 5.184 / 576 / 374 / 21 / 2.248 | 5.232 / 584 / 381 / 22 / 2.184 |
| Oranice u klasama 1–3 | 971 oranica, 1.935 ha | 987 oranica, 1.971 ha |
| Referentna srednja vrijednost i st. devijacija dNDVI | −0,0262 / 0,1887 | −0,0243 / 0,1851 |

- Među oranicama ocijenjenima u obje obrade 98,6 % ima istu klasu, a nijedna se ne razlikuje za više od jedne klase.
- Srednji dNDVI po parceli: korelacija 0,994, medijan apsolutne razlike 0,004.
- Male razlike potječu od mreže piksela: QGIS sve računa na mreži od točno 10 m, a u testu je snimka od 7. 7.
  preprojicirana sa zadanom veličinom piksela 10,34 m.
- Pojas tuče u QGIS-u čine skupine od najmanje 50 povezanih piksela ispod praga (1.697 ha). Pojas služi za prikaz;
  klase štete ne ovise o njemu.

## Pokretanje

QGIS 3.28 ili noviji (Windows: OSGeo4W Shell; Linux: `python3`):

```
python3 qgis_poplava.py ulaz_poplava izlaz_poplava
python3 qgis_tuca.py <SAFE 22. 6.> <SAFE 7. 7.> jls_tuca.gpkg arkod_2024.gpkg izlaz_tuca
```
