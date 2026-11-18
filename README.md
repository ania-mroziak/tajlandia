# Bangkok i Koh Phangan

Przewodnik po Bangkoku i Koh Phangan: dwie mapy z klikalnymi punktami, plan na 3 dni w Bangkoku i 4 dni na Phanganie, wszystkie miejsca z linkami do Map Google.

Strona: https://ania-mroziak.github.io/tajlandia/

Cała strona to jeden plik `index.html` (bez zewnętrznych bibliotek, tylko czcionki z Google Fonts).

## Jak zaktualizować
1. Zmień dane w `zrodla/places.json` (Koh Phangan) albo `zrodla/bkk.json` (Bangkok). Bangkok: współrzędne i kategorie są w `zrodla/build_guide.py`.
2. Uruchom `./zrodla/zbuduj.sh`.
3. Zrób commit i push. GitHub Pages zaktualizuje stronę w 1–2 minuty.
