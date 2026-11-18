#!/usr/bin/env bash
# Buduje index.html z danych w tym folderze (places.json = Koh Phangan, bkk.json = Bangkok).
set -euo pipefail
cd "$(dirname "$0")"
python3 -I build_guide.py "$PWD" "$PWD/strona.html"
python3 -I - <<'PY'
t=open("strona.html").read(); i=t.index("</style>")+len("</style>")
head='<!doctype html>\n<html lang="pl">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<style>[hidden]{display:none!important} body{margin:0} img{max-width:100%}</style>\n'
open("../index.html","w").write(head+t[:i]+"\n</head>\n<body>\n"+t[i:]+"\n</body>\n</html>\n")
PY
rm -f strona.html .podglad.html
echo "Gotowe: index.html"
