# ============================================================
# Datei: wildtierkompass/admin.py
# Zweck: Legt fest, welche Models im Admin erscheinen und wie.
# ============================================================

from django.contrib import admin

# NEU: Kategorie zusätzlich importieren, sonst kennt admin.py sie nicht
from .models import Antwort, Frage, Kategorie, Tierart


class AntwortInline(admin.TabularInline):
    """Zeigt die Antworten direkt INNERHALB der Frage an.
    So pflegst du eine Frage und ihre Antworten auf einer Seite."""

    model = Antwort
    # Pflicht, weil Antwort zwei Fremdschlüssel auf Frage hat.
    # Wir sagen Django: Gruppiere über das Feld "frage".
    fk_name = "frage"
    extra = 2  # zwei leere Zeilen für neue Antworten, z. B. Ja und Nein


@admin.register(Frage)
class FrageAdmin(admin.ModelAdmin):
    inlines = [AntwortInline]
    list_display = ["text", "tierart"]  # Spalten in der Übersicht
    list_filter = ["tierart"]           # Filter rechts nach Tierart


# NEU: Kategorie im Admin anmelden.
# Ohne diese Zeilen könntest du keine Kategorien anlegen.
# Eine leere Klasse reicht, Django nutzt dann die Standardansicht.
@admin.register(Kategorie)
class KategorieAdmin(admin.ModelAdmin):
    pass


@admin.register(Tierart)
class TierartAdmin(admin.ModelAdmin):
    # NEU: "kategorie" als Spalte in der Übersicht
    list_display = ["name", "kategorie", "start_frage"]
    # NEU: Filter rechts, um z. B. nur Vögel anzuzeigen.
    # Hilfreich, sobald es viele Tierarten gibt.
    list_filter = ["kategorie"]