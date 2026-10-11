# 🦔 Wildtierkompass

> [!IMPORTANT]
> 🚧 **Dieses Projekt befindet sich im Aufbau.**
> Aktuell ist nur der Leitfaden für den Igel vollständig.
> Weitere Tierarten und Funktionen folgen schrittweise.

Ein Leitfaden für Laien, die ein Wildtier gefunden haben.
Über einfache Fragen führt die App zu einer Handlungsempfehlung
mit Dringlichkeitsampel, Tipps und seriösen Anlaufstellen.

Lernprojekt im Rahmen meiner Umschulung zur
Fachinformatikerin für Anwendungsentwicklung.

## Funktionen

- Entscheidungsbaum je Tierart, gepflegt über den Django Admin
- Dringlichkeitsampel von "In Ruhe lassen" bis "Notfall"
- Tipps, Tabus und Quellen je Tierart
- Gruppierung nach Kategorien, z. B. Säugetiere und Vögel

## Geplant

- Weitere Tierarten, z. B. Singvögel, Mauersegler, Stadttauben, Eichhörnchen
- Besondere Hinweise für Tiere, die unter das Jagdrecht fallen, z. B. Reh, Fuchs und Hase
- Tipps, wie man gesunde Wildtiere im Alltag unterstützen kann
- Validierung, damit jede Antwort zu einer Frage oder Empfehlung führt
- Anlaufstellen in der Nähe, z. B. Wildtierstationen und Tierärzte

## Technik

- Python, Django
- SQLite
- Django Templates mit eigenem CSS

## Installation (Windows)

```powershell
git clone https://github.com/sudo-mach-hinne/Wildtierkompass.git
cd Wildtierkompass
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python -X utf8 manage.py loaddata daten.json
python manage.py createsuperuser
python manage.py runserver
```

Danach im Browser öffnen: http://127.0.0.1:8000/

## Hinweis

Dieser Leitfaden ersetzt keine tierärztliche Beratung.
Die Inhalte stützen sich auf Empfehlungen von Pro Igel e.V. und NABU.