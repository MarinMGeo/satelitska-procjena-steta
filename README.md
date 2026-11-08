# Satelitska procjena šteta: poplava i tuča

Web aplikacija za procjenu štete od prirodnih nepogoda na poljoprivrednim (ARKOD) parcelama iz satelitskih snimaka Copernicus. Obrađena su dva događaja, a između njih se bira jednim klikom:

- **Poplava** Kupe i Korane, svibanj 2023., Karlovac, Duga Resa, Barilović i Lasinja: radar Sentinel-1 i optika Sentinel-2.
- **Tuča** 1. 7. 2024., Gradište, Županja i Štitar s pojasom od 5 km: optika Sentinel-2 (22. 6. i 7. 7. 2024.) i prijave tuče iz baze ESWD.

Rad za Datathon Portala otvorenih podataka 2026, izazov B (Okoliš i održivi prostor).

## Što aplikacija radi

- Na karti prikazuje obuhvat poplave i 3.892 ARKOD parcele u kojima je otkrivena voda, obojene po razredu poplavljenosti ili po šteti po hektaru.
- Klik na parcelu ili upis ARKOD ID-a otvara karticu parcele s ovim podacima:
  - vrsta uporabe i poplavljena površina;
  - radarski potpis kroz tri datuma (5. 5., 17. 5. i 29. 5.);
  - izračun štete po formuli: *poplavljena površina × prinos × cijena × gubitak prinosa*.
- Optička provjera (Sentinel-2): snimke u prirodnim bojama prije (5. 5.) i poslije (22. 5. 2023.) s klizačem za usporedbu, karta promjene vegetacije (NDVI) i vode ili mokrog tla.
- Gubitak prinosa mjeri se za svaku poplavljenu parcelu iz pada NDVI-ja u odnosu na nepoplavljene parcele iste vrste uporabe (kontrolni skup). Umjesto toga mogu se odabrati scenariji 25, 50 ili 100 %.
- Cijene i prinose po vrsti uporabe zemljišta korisnik mijenja u tablici, a izračun se odmah osvježava. Početne cijene su iz Prijedloga jedinstvenih cijena za Registar šteta 2026./2027.
- Zbroj po JLS odgovara načinu prijave u Registar šteta.
- Alat **Prag detekcije** ponovno izračunava obuhvat poplave u pregledniku za bilo koje pragove. Uključuje i automatski prag po Otsuovoj metodi.
- Izvoz u CSV (sve pogođene parcele ili zbroj po JLS) za Excel. Separator je točka-zarez, a decimalni znak zarez.

## Struktura

```
docs/            gotova statička aplikacija (index.html + data/), objavljuje se na GitHub Pages
pipeline/        Python skripta koja iz ArcGIS File Geodatabase rezultata izrađuje web podatke
arcgis/          povijest geoprocesiranja iz ArcGIS Pro (izvorna analiza)
src/             izvorni HTML; build.py ga sastavlja u docs/index.html
```

## Pokretanje

Lokalno:

```
cd site
python -m http.server 8000
```

Zatim otvorite `http://localhost:8000` u pregledniku.

Za objavu na GitHub Pages: Settings → Pages → Source: *Deploy from a branch*, grana `main`, mapa `/docs`.

Ponovna izrada podataka iz geobaze:

```
pip install -r pipeline/requirements.txt
python pipeline/izvoz_web_podataka.py "putanja/do/DATATHON_poplave.gdb" docs/data
```

Skripta čita File Geodatabase izravno, bez ArcGIS-a: vektore preko GDAL-a, a rastere vlastitim čitačem blokova.

Optički dio (Sentinel-2 L2A, pojasevi od 20 m: B03, B04, B8A, B11, SCL, TCI):

```
python pipeline/optika_sentinel2.py "mapa/sa/SAFE/produktima" "putanja/do/DATATHON_poplave.gdb" docs/data
```

## Tuča (Županja, 1. 7. 2024.)

1. Sentinel-2 L2A (T33TYL) 22. 6. i 7. 7. 2024. Indeksi NDVI, NDRE, NDMI, MSAVI2, PSRI i BSI.
2. Maska žetve (nizak NDVI prije ili golo tlo poslije), pa prag na dNDVI, zaglađivanje (Majority, RegionGroup) i poligon pojasa tuče.
3. ARKOD oranice suzene za 10 m. Zonalna statistika dNDVI-ja i z-vrijednost prema referentnim parcelama. Klase 1–3 za z ≤ −1, −2 i −3.
4. Gubitak prinosa iz NDVI-ja u odnosu na oranice izvan pojasa tuče, cijene iz Registra šteta.
5. Potvrda događaja: European Severe Weather Database (ESWD), tuča 4,5–6,5 cm, 1. 7. 2024. oko 17:10 UTC.

```
python pipeline/tuca_web.py klase_stete_rez Indeksi_i_delte jls.geojson mapa_sa_SAFE docs/data/tuca
```

## Metoda (poplava)

1. Sentinel-1A GRD (IW, VV) za tri datuma iste putanje: kalibracija, filtriranje, terenska korekcija, pretvorba u dB, piksel 10 m, HTRS96/TM.
2. Detekcija promjene. Piksel je poplavljen ako vrijede sva tri uvjeta:
   - VV na dan 17. 5. manji je od −16 dB;
   - pad u odnosu na 5. 5. veći je od 3 dB;
   - porast do 29. 5. veći je od 3 dB.
3. Maska je pretvorena u poligone, a dijelovi manji od 0,05 ha su uklonjeni. Ostalo je 1.528 poligona, ukupno oko 1.503 ha.
4. Presjek s ARKOD parcelama 2024. daje poplavljenu površinu, postotak i razred za svaku parcelu:
   - 1: do 25 %;
   - 2: 25–50 %;
   - 3: 50–75 %;
   - 4: više od 75 %.
5. Sentinel-2 za 12. 5. 2022. (normalna godina), 5. 5. 2023. (prije) i 22. 5. 2023. (poslije). Obrada uključuje sljedeće:
   - refleksija je ispravljena za pomak −1000;
   - oblaci, sjene i cirus maskirani su prema SCL-u (3, 8, 9 i 10);
   - MNDWI pokazuje vodu i mokro tlo;
   - NDVI pokazuje stanje vegetacije.
6. Potvrda: 22. 5. na 39 % radarski poplavljene površine još je voda ili mokro tlo, a 5. 5. bilo ih je samo na 3 %. NDVI je na poplavljenim pikselima pao za 0,30 (medijan), a na ostalima se nije promijenio.
7. Gubitak prinosa po parceli: pad NDVI-ja veći od uobičajene promjene na nepoplavljenim parcelama iste vrste uporabe (medijan i MAD), podijeljen s NDVI-jem prije poplave (najmanje 0,15), ograničen na 0–1. Primjenjuje se samo uz z < −1. Za oranice koje su 5. 5. bile golo tlo (NDVI < 0,3) i parcele pod oblacima gubitak se ne može izmjeriti i uzima se 50 %.
8. Šteta = poplavljena površina × prinos × cijena iz Registra šteta × gubitak prinosa.

## Pouzdanost

Bez terenskog očevida pouzdanost se procjenjuje neovisnim mjerenjima (`pipeline/validacija.py`, rezultat u `docs/data/validacija.json`, prikaz u kartici **Pouzdanost**):

- **Poplava:** radar (Sentinel-1) prema optici (Sentinel-2, 22. 5.) po parcelama daje preciznost 87 % i kappa 0,51, a po pikselima kappa 0,35, jer se voda u međuvremenu povlačila. Osjetljivost na prag: od 908 ha (strogo) do 2.579 ha (blago).
- **Tuča:** NDVI se slaže s neovisnim indeksima NDRE (kappa 0,85) i NDMI (kappa 0,73). Najveća nesigurnost je izbor referentnih parcela: 1.971 ha i 1,6 mil. € (studenti, konzervativno) prema 5.383 ha i 3,1 mil. € (referenca izvan pojasa). Prijava tuče iz ESWD-a nalazi se 340 m od pojasa tuče.
- Aplikacija izvozi stratificirani slučajni uzorak parcela za terensku provjeru. Iz njega nastaje prava matrica konfuzije.

## Otvoreni podaci

- Copernicus Sentinel-1 i Sentinel-2 (ESA, Copernicus Data Space Ecosystem)
- ARKOD 2024 (Agencija za plaćanja u poljoprivredi, ribarstvu i ruralnom razvoju)
- Granice JLS i digitalni ortofoto (Državna geodetska uprava)
- Vodna tijela (Hrvatske vode)
- Global Surface Water (Europska komisija, JRC)
- Prijedlog jedinstvenih cijena za Registar šteta 2026./2027. (DZS, TISUP)
- European Severe Weather Database (ESWD), European Severe Storms Laboratory

## Licencija

Kod je pod licencijom EUPL-1.2 (datoteka `LICENSE`). Podaci zadržavaju licencije svojih izvora.

## Tim

GEOtim2, Geografski odsjek, Prirodoslovno-matematički fakultet Sveučilišta u Zagrebu. Mentor: doc. dr. sc. Marin Mićunović.
