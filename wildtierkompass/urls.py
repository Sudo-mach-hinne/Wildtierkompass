# ============================================================
# Datei: wildtierkompass/urls.py  (diese Datei legst du selbst an)
# Zweck: Das "Adressbuch" der App. Hier steht, welche Adresse
#        zu welcher View führt.
# Wer liest sie? config/urls.py bindet sie mit include() ein.
# ============================================================

# path() verknüpft ein Adressmuster mit einer View.
from django.urls import path

# Wir importieren das ganze Modul views, damit wir unten
# views.start, views.frage usw. schreiben können.
from . import views

# Namensraum der App.
# Warum? In größeren Projekten haben mehrere Apps vielleicht eine URL
# namens "start". Mit dem Namensraum heißt unsere eindeutig
# "wildtierkompass:start". So nutzen wir sie in Views und Templates.
app_name = "wildtierkompass"

# Django geht diese Liste von oben nach unten durch und nimmt
# den ERSTEN Eintrag, der zur aufgerufenen Adresse passt.
urlpatterns = [
    # path(muster, view, name=...)
    #   muster: der Teil der Adresse NACH http://127.0.0.1:8000/
    #   view:   die Funktion, die aufgerufen wird (ohne Klammern!)
    #   name:   interner Name, über den wir die URL ansprechen

    # Leeres Muster "" = Startseite
    path("", views.start, name="start"),

    # <int:pk> ist ein Platzhalter.
    #   int: nur ganze Zahlen passen, /frage/abc/ würde nicht passen
    #   pk:  unter diesem Namen landet die Zahl als Parameter in der View
    path("frage/<int:pk>/", views.frage, name="frage"),

    path("antwort/<int:pk>/", views.antwort, name="antwort"),
]