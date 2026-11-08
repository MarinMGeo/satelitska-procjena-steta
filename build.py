"""Sastavlja docs/index.html iz src/index.src.html i umeće Leaflet CSS."""
import pathlib
R=pathlib.Path(__file__).parent
s=(R/"src/index.src.html").read_text()
css=(R/"src/leaflet.min.css").read_text()
page=s.replace("/*__LEAFLET_CSS__*/",css)
full='<!doctype html>\n<html lang="hr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
head,body=page.split("</style>",1)
full+=head+"</style>\n</head>\n<body>\n"+body+"\n</body>\n</html>\n"
(R/"docs").mkdir(exist_ok=True); (R/"docs/index.html").write_text(full)
print("ok",len(page))
