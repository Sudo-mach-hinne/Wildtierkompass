from django.db import models


# NEU: Die Kategorie steht ganz oben, weil Tierart auf sie verweist.
# Steht eine Klasse VOR ihrer Verwendung, brauchen wir keine
# Anführungszeichen wie bei "Frage" weiter unten.
class Kategorie(models.Model):
    """Oberbegriff für Tierarten, z. B. Vögel oder Säugetiere."""

    # unique=True: Jeder Kategoriename darf nur einmal vorkommen.
    # Warum? Zweimal "Vögel" würde Laien auf der Startseite verwirren.
    # Die Datenbank legt dafür einen UNIQUE Constraint an.
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Kategorie"
        verbose_name_plural = "Kategorien"
        # ordering legt die Standardsortierung fest.
        # Jede Abfrage ohne eigenes order_by() wird automatisch nach
        # Namen sortiert, auch im Admin und im Template.
        ordering = ["name"]

    def __str__(self):
        return self.name


class Tierart(models.Model):
    """Eine Tierart, für die es einen Entscheidungsbaum gibt (UC1)."""

    # NEU: Zu welcher Kategorie gehört die Tierart? (1:n Beziehung)
    # Eine Kategorie hat viele Tierarten, jede Tierart hat eine Kategorie.
    #
    # on_delete=PROTECT: Eine Kategorie kann NICHT gelöscht werden,
    # solange noch Tierarten dazugehören. Django zeigt dann einen Fehler.
    # Warum nicht CASCADE? Sonst würde das Löschen von "Vögel" alle
    # Vogel Entscheidungsbäume mitlöschen. Das wäre ein großer Datenverlust.
    #
    # null=True: Nötig, weil der Igel schon in der DB steht und noch
    # keine Kategorie hat. Ohne null=True würde makemigrations fragen,
    # welche Kategorie er bekommen soll, und die gibt es noch gar nicht.
    #
    # related_name="tierarten" erlaubt später kategorie.tierarten.all()
    kategorie = models.ForeignKey(
        Kategorie,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="tierarten",
    )

    # CharField = kurzer Text mit Maximallänge, wird zu VARCHAR in der DB
    name = models.CharField(max_length=100)

    # TextField = langer Text ohne Längenbegrenzung
    # blank=True erlaubt, dass das Feld im Formular leer bleiben darf
    beschreibung = models.TextField(blank=True)

    # Allgemeine Hinweise und Tabus zu dieser Tierart,
    # z. B. "Niemals Milch geben". Sie erscheinen bei JEDER Empfehlung
    # dieser Tierart, damit sie nicht in jeder Antwort wiederholt werden müssen.
    tipps = models.TextField(blank=True, default="", verbose_name="Tipps und Tabus")

    # Woher stammt das Wissen? Schafft Vertrauen bei den Nutzern.
    # Links und E-Mail-Adressen werden im Template automatisch klickbar.
    quelle = models.TextField(blank=True, default="", verbose_name="Quellen")

    # Mit dieser Frage beginnt der Entscheidungsbaum.
    # "Frage" steht in Anführungszeichen, weil die Klasse erst weiter unten
    # definiert wird. Django löst den Namen später auf.
    # null=True: Die Spalte darf in der DB leer sein, denn beim Anlegen
    # der Tierart gibt es die Startfrage oft noch nicht.
    # on_delete=SET_NULL: Wird die Frage gelöscht, bleibt die Tierart
    # erhalten und das Feld wird einfach geleert.
    start_frage = models.ForeignKey(
        "Frage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",  # "+" = keine Rückwärtsbeziehung nötig
    )

    class Meta:
        # So heißt die Tabelle im Admin, statt "Tierarts"
        verbose_name = "Tierart"
        verbose_name_plural = "Tierarten"
        # NEU: Tierarten immer alphabetisch sortieren.
        # Warum hier und nicht in der View? Weil das Template später
        # kategorie.tierarten.all aufruft. Dort können wir kein order_by
        # anhängen, also muss die Sortierung im Model stehen.
        ordering = ["name"]

    def __str__(self):
        # Bestimmt, wie ein Objekt angezeigt wird, z. B. in Auswahllisten.
        # Ohne diese Methode stünde dort "Tierart object (1)".
        return self.name


class Frage(models.Model):
    """Eine Frage im Entscheidungsbaum (UC2)."""

    # Jede Frage gehört zu genau einer Tierart (1:n).
    # on_delete=CASCADE: Wird die Tierart gelöscht, verschwinden
    # ihre Fragen mit, denn ohne Tierart sind sie sinnlos.
    tierart = models.ForeignKey(
        Tierart,
        on_delete=models.CASCADE,
        related_name="fragen",  # erlaubt später igel.fragen.all()
    )
    text = models.CharField(max_length=300)

    class Meta:
        verbose_name = "Frage"
        verbose_name_plural = "Fragen"

    def __str__(self):
        return f"{self.tierart}: {self.text}"


class Antwort(models.Model):
    """Eine Antwortmöglichkeit auf eine Frage (UC2 und UC3)."""

    # Die erlaubten Stufen der Dringlichkeit.
    # TextChoices ist eine Aufzählung (Enum) von Django.
    # Jede Zeile hat zwei Teile:
    #   links:  der Wert, der in der Datenbank gespeichert wird ("notfall")
    #   rechts: der Anzeigename für Menschen ("Notfall")
    # Warum nicht einfach Freitext? Mit festen Werten kann sich niemand
    # vertippen, und das Template kann jedem Wert eine Farbe zuordnen.
    class Dringlichkeit(models.TextChoices):
        NOTFALL = "notfall", "Notfall"
        DRINGEND = "dringend", "Dringend"
        ABKLAEREN = "abklaeren", "Abklären lassen"
        BEOBACHTEN = "beobachten", "Beobachten"
        IN_RUHE = "in_ruhe", "In Ruhe lassen"

    # Zu welcher Frage gehört diese Antwort?
    # related_name="antworten" erlaubt später frage.antworten.all()
    frage = models.ForeignKey(
        Frage,
        on_delete=models.CASCADE,
        related_name="antworten",
    )
    text = models.CharField(max_length=100)

    # Weg A: Es geht mit einer weiteren Frage weiter.
    # Ein eigener related_name ist hier Pflicht, weil Antwort ZWEI
    # Fremdschlüssel auf Frage hat. Ohne unterschiedliche Namen wüsste
    # Django nicht, welche Beziehung frage.antwort_set meint.
    naechste_frage = models.ForeignKey(
        Frage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vorherige_antworten",
    )

    # Weg B: Der Baum endet hier mit einer Handlungsempfehlung (UC3).
    empfehlung = models.TextField(blank=True)

    # Wie dringend ist die Lage? Wird als farbige Ampel angezeigt.
    # choices=... macht im Admin automatisch ein Dropdown daraus.
    # blank=True, weil nur Antworten MIT Empfehlung eine Dringlichkeit
    # brauchen. Antworten, die zur nächsten Frage führen, bleiben leer.
    dringlichkeit = models.CharField(
        max_length=20,
        choices=Dringlichkeit.choices,
        blank=True,
        default="",
    )

    class Meta:
        verbose_name = "Antwort"
        verbose_name_plural = "Antworten"

    def __str__(self):
        return f"{self.frage.text} -> {self.text}"