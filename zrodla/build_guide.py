import json, sys, math
D, OUT = sys.argv[1], sys.argv[2]

# ---------- Koh Phangan ----------
geo = json.load(open(D + "/geo.json"))
php = json.load(open(D + "/places.json"))
Cp = math.cos(math.radians(9.73)); Sp = 6000
def Pp(lat, lng): return [round((lng - 99.93) * Cp * Sp, 1), round((9.815 - lat) * Sp, 1)]
for p in php["places"]:
    p["x"], p["y"] = Pp(p["lat"], p["lng"])
php_cfg = {
    "full": [0, 0, 1005, 930], "allName": "Cała wyspa",
    "areas": php["areas"], "places": php["places"], "plan": php["plan"], "plan_extra": php.get("plan_extra", ""),
    "cats": [
        {"id": "plaze", "name": "Plaże, widoki, natura", "col": "plaze"},
        {"id": "jedzenie", "name": "Jedzenie", "col": "jedzenie"},
        {"id": "kawa", "name": "Kawa i śniadania", "col": "kawa"},
        {"id": "wellness", "name": "Joga, masaż, sauna", "col": "wellness"},
        {"id": "sport", "name": "Sport", "col": "sport"},
        {"id": "impreza", "name": "Impreza", "col": "impreza"},
        {"id": "prom", "name": "Port", "col": "prom"},
    ],
    "labels": [[k, v[0], v[1], ""] for k, v in geo["labels"].items()] + [["↓ Koh Samui, ok. 20 km promem", 330, 905, ""]],
}

# ---------- Bangkok ----------
bg = json.load(open(D + "/bkkgeo.json"))
x0, y1 = 100.47, 13.88
Cb = math.cos(math.radians(13.8)); Sb = 6600
def Pb(lat, lng): return [round((lng - x0) * Cb * Sb, 1), round((y1 - lat) * Sb, 1)]
src = json.load(open(D + "/bkk.json"))
items = {it["name"]: it for g in src["groups"] for it in g["items"]}
def B(name, area, cat, lat, lng, newname=None, extra=""):
    it = dict(items[name]); it.pop("col", None)
    it["name"] = newname or name; it["area"] = area; it["cat"] = cat
    it["lat"], it["lng"] = lat, lng; it["x"], it["y"] = Pb(lat, lng)
    if extra: it["text"] = it["text"] + " " + extra
    return it
bkk_places = [
    B("Wielki Pałac Królewski", "stare", "swiatynie", 13.7498558, 100.4915765),
    B("Wat Pho", "stare", "swiatynie", 13.7464237, 100.4927733),
    B("Wat Arun", "stare", "swiatynie", 13.7438652, 100.488444),
    B("Thipsamai", "stare", "jedzenie", 13.7527976, 100.504823),
    B("Rajadamnern Stadium", "stare", "sport", 13.7609937, 100.5087949, extra="Bilet kupcie online, wcześniej."),
    B("Khao San Road", "stare", "zwiedzanie", 13.7581072, 100.4989781),
    B("Chinatown (Yaowarat)", "stare", "zwiedzanie", 13.7408624, 100.5086773),
    B("Yokkao Training Center", "centrum", "sport", 13.7286843, 100.5605017),
    B("Park Lumpini", "centrum", "zwiedzanie", 13.7314281, 100.5416984),
    B("Khao-Sō-i", "centrum", "jedzenie", 13.7273, 100.5335),
    B("Siam Center", "centrum", "zakupy", 13.7462793, 100.5326779),
    B("Tichuca Rooftop Bar", "centrum", "bar", 13.7223968, 100.5805317),
    B("After You", "centrum", "deser", 13.7379, 100.5604, newname="After You (kakigori)"),
    B("Chatuchak Weekend Market", "polnoc", "zakupy", 13.799781, 100.5504245),
    B("MOCA Bangkok", "polnoc", "zwiedzanie", 13.8523198, 100.5630092),
    B("One Lumpinee", "polnoc", "sport", 13.8666496, 100.608311, extra="Bilet kupcie online, wcześniej."),
]
names = {p["name"] for p in bkk_places}
rename = {"After You": "After You (kakigori)"}
plan = []
for d in src["plan"]:
    steps = []
    for s in d["steps"]:
        ps = [rename.get(n, n) for n in s["l"]]
        ps = [n for n in ps if n in names]
        steps.append({"t": s["t"], "p": ps})
    plan.append({"day": d["day"], "title": d["title"], "steps": steps})
# river label: a point of the river roughly at lat 13.80
rpts = [tuple(map(float, xy.split(","))) for xy in bg["river"].replace("M", " ").replace("L", " ").split()]
target_y = Pb(13.80, 100.5)[1]
rx, ry = min(rpts, key=lambda t: abs(t[1] - target_y))
labels = [
    ["Chao Phraya", round(rx - 70, 1), round(ry, 1), "water"],
    ["Stare miasto", *Pb(13.770, 100.494), ""],
    ["Siam", *Pb(13.7535, 100.5327), ""],
    ["Silom", *Pb(13.7205, 100.527), ""],
    ["Sukhumvit", *Pb(13.746, 100.578), ""],
    ["Chatuchak", *Pb(13.809, 100.5504), ""],
]
bkk_cfg = {
    "full": [0, 0, 993, 1089], "allName": "Całe miasto",
    "areas": [
        {"id": "stare", "name": "Stare miasto i Chinatown", "sub": "świątynie, pad thai, Khao San i gala Muay Thai",
         "warn": [g for g in src["groups"] if g["id"] == "swiatynie"][0]["warn"]},
        {"id": "centrum", "name": "Centrum: Siam, Silom, Sukhumvit", "sub": "park, zupka, zakupy, kakigori, trening i rooftop"},
        {"id": "polnoc", "name": "Północ", "sub": "targ weekendowy, muzeum i druga gala"},
    ],
    "cats": [
        {"id": "swiatynie", "name": "Świątynie", "col": "wellness"},
        {"id": "zwiedzanie", "name": "Zwiedzanie", "col": "plaze"},
        {"id": "jedzenie", "name": "Jedzenie", "col": "jedzenie"},
        {"id": "deser", "name": "Desery", "col": "kawa"},
        {"id": "sport", "name": "Muay Thai", "col": "sport"},
        {"id": "zakupy", "name": "Zakupy", "col": "impreza"},
        {"id": "bar", "name": "Wieczór", "col": "prom"},
    ],
    "places": bkk_places, "plan": plan, "labels": labels,
}

t = open(D + "/guide_template.html").read()
data = {"bangkok": bkk_cfg, "phangan": php_cfg}
for k, v in {"{{PATH}}": geo["path"], "{{ZONE}}": geo["zone"], "{{RIVER}}": bg["river"],
             "{{N_BKK}}": str(len(bkk_places)), "{{N_PHP}}": str(len(php["places"])),
             "{{DATA}}": json.dumps(data, ensure_ascii=False)}.items():
    assert k in t, k
    t = t.replace(k, v)
open(OUT, "w").write(t)
open(OUT.rsplit("/", 1)[0] + "/.podglad.html", "w").write(
    '<!doctype html><html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>[hidden]{display:none!important}</style></head><body>' + t + '</body></html>')
print("Bangkok:", len(bkk_places), "| Phangan:", len(php["places"]), "| rozmiar:", len(t))
