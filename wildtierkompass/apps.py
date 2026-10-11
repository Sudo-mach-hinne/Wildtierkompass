from django.apps import AppConfig


class WildtierkompassConfig(AppConfig):
    """Konfiguration der App. Django liest diese Klasse beim Start ein."""

    # Standardtyp für automatisch erzeugte Primärschlüssel (id Spalte)
    default_auto_field = "django.db.models.BigAutoField"

    # Muss exakt dem Ordnernamen entsprechen, denn Django importiert
    # die App über diesen Namen. Hier lag der Fehler.
    name = "wildtierkompass"

    # Anzeigename im Admin, rein kosmetisch
    verbose_name = "Wildtierkompass"