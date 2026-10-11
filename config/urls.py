# ============================================================
# Datei: config/urls.py
# Zweck: Das zentrale "Adressbuch" des gesamten Projekts.
#        Jede Anfrage landet ZUERST hier. Von hier aus wird sie
#        an den Admin oder an unsere App weitergereicht.
# ============================================================

# admin: der eingebaute Verwaltungsbereich von Django
from django.contrib import admin
# include: bindet eine andere urls.py ein (hier die unserer App)
from django.urls import include, path

urlpatterns = [
    # Alles, was mit /admin/ beginnt, geht an den Django Admin.
    path("admin/", admin.site.urls),

    # Alle anderen Adressen gibt das Projekt an unsere App weiter.
    # Warum include()? So bleibt jede App für ihre eigenen URLs
    # zuständig. Das Projekt muss die Details nicht kennen.
    # Beispiel: /frage/3/ wird hier nicht gefunden, also schaut Django
    # in wildtierkompass/urls.py und findet dort "frage/<int:pk>/".
    path("", include("wildtierkompass.urls")),
]