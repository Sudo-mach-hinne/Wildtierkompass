# ============================================================
# Datei: wildtierkompass/views.py
# Zweck: Views sind die "Steuerzentrale" jeder Seite.
#        Eine View ist eine Python Funktion, die eine Anfrage
#        (request) vom Browser bekommt, Daten aus der Datenbank
#        holt und eine Antwort (response) zurückgibt.
# Wer ruft sie auf? Django, sobald eine URL aus urls.py passt.
# ============================================================

# get_object_or_404: holt GENAU EIN Objekt aus der DB oder zeigt
#   "Seite nicht gefunden" (HTTP 404), falls es nicht existiert.
# redirect: schickt den Browser zu einer anderen Adresse weiter.
# render: verbindet ein Template mit Daten und erzeugt fertiges HTML.
from django.shortcuts import get_object_or_404, redirect, render

# NEU: Kategorie zusätzlich importieren
from .models import Antwort, Frage, Kategorie, Tierart


def start(request):
    """UC1: Startseite, zeigt alle Tierarten gruppiert nach Kategorie.

    Erreichbar unter: http://127.0.0.1:8000/
    """
    # NEU: Alle Kategorien holen. Sortiert sind sie automatisch nach
    # Namen, weil im Model ordering = ["name"] steht.
    # Die Tierarten je Kategorie holt sich das Template selbst über
    # kategorie.tierarten.all (dank related_name="tierarten").
    kategorien = Kategorie.objects.all()

    # NEU: Tierarten, die noch KEINER Kategorie zugeordnet sind.
    # Warum? Sonst würden sie auf der Startseite einfach verschwinden.
    # kategorie__isnull=True bedeutet: das Feld kategorie ist leer.
    # Der doppelte Unterstrich __ ist Djangos Schreibweise für
    # Bedingungen ("Lookups"). Entspricht in SQL:
    #   SELECT * FROM wildtierkompass_tierart WHERE kategorie_id IS NULL;
    ohne_kategorie = Tierart.objects.filter(kategorie__isnull=True)

    # Beide Listen kommen in den Context und sind im Template
    # unter diesen Namen verfügbar.
    return render(
        request,
        "wildtierkompass/start.html",
        {"kategorien": kategorien, "ohne_kategorie": ohne_kategorie},
    )


def frage(request, pk):
    """UC2: Zeigt eine Frage mit ihren Antwortmöglichkeiten.

    Erreichbar unter: http://127.0.0.1:8000/frage/<nummer>/
    """
    # pk (primary key) kommt aus der URL. Bei /frage/3/ ist pk = 3.
    frage = get_object_or_404(Frage, pk=pk)

    # Die Antworten holt sich das Template selbst über
    # frage.antworten.all, dank related_name="antworten".
    return render(request, "wildtierkompass/frage.html", {"frage": frage})


def antwort(request, pk):
    """UC2 und UC3: Entscheidet, wie es nach einer gewählten Antwort weitergeht.

    Erreichbar unter: http://127.0.0.1:8000/antwort/<nummer>/
    """
    antwort = get_object_or_404(Antwort, pk=pk)

    # Weg A: Die Antwort verweist auf eine Folgefrage, also weiterleiten.
    if antwort.naechste_frage:
        return redirect("wildtierkompass:frage", pk=antwort.naechste_frage.pk)

    # Weg B: Keine Folgefrage, der Baum endet hier mit der Empfehlung.
    return render(request, "wildtierkompass/empfehlung.html", {"antwort": antwort})