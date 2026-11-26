from django.db import models
from django.utils.text import slugify

from .i18n import TranslatedMixin, add_translated


class Timestamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SampleFlag(models.Model):
    """Marks placeholder content that OPMT still has to confirm or replace."""

    is_sample = models.BooleanField(
        "Dadus ezemplu", default=False,
        help_text="Marka se dadus ne'e seidauk konfirma husi OPMT.",
    )

    class Meta:
        abstract = True


class SiteSetting(TranslatedMixin, Timestamped):
    """Single row with organisation-wide information."""

    name = models.CharField(max_length=120, default="Organização Popular da Mulher Timor")
    short_name = models.CharField(max_length=20, default="OPMT")
    founded = models.DateField(null=True, blank=True)
    add_translated(locals(), "tagline")
    add_translated(locals(), "about", kind="text")
    add_translated(locals(), "mission", kind="text")
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=60, blank=True)
    email = models.EmailField(blank=True)
    facebook = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    logo = models.ImageField(upload_to="site/", blank=True)

    class Meta:
        verbose_name = "Konfigurasaun website"
        verbose_name_plural = "Konfigurasaun website"

    def __str__(self):
        return self.short_name

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Objective(TranslatedMixin, models.Model):
    """Objectives from the OPMT statutes (Art. 4-5)."""

    KIND = [("general", "Objetivu jerál"), ("specific", "Objetivu espesífiku")]
    kind = models.CharField(max_length=10, choices=KIND, default="specific")
    order = models.PositiveIntegerField(default=0)
    add_translated(locals(), "text", kind="text", required=True)

    class Meta:
        ordering = ["kind", "order"]
        verbose_name = "Objetivu"
        verbose_name_plural = "Objetivu sira"

    def __str__(self):
        return self.text_tet[:60]


class HistoryEvent(TranslatedMixin, SampleFlag, Timestamped):
    CATEGORY = [
        ("foundation", "Fundasaun"),
        ("resistance", "Rezisténsia"),
        ("independence", "Independénsia"),
        ("organisation", "Organizasaun"),
        ("achievement", "Susesu"),
    ]
    year = models.PositiveIntegerField()
    date = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY, default="organisation")
    add_translated(locals(), "title", required=True)
    add_translated(locals(), "body", kind="text")
    image = models.ImageField(upload_to="history/", blank=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["year", "order"]
        verbose_name = "Eventu istória"
        verbose_name_plural = "Istória (linha tempu)"

    def __str__(self):
        return f"{self.year} – {self.title_tet}"


class Figure(TranslatedMixin, SampleFlag, Timestamped):
    """Heroines and historic figures of OPMT."""

    name = models.CharField(max_length=150)
    nickname = models.CharField(max_length=80, blank=True)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    add_translated(locals(), "role")
    add_translated(locals(), "bio", kind="text")
    birth_year = models.PositiveIntegerField(null=True, blank=True)
    death_year = models.PositiveIntegerField(null=True, blank=True)
    photo = models.ImageField(upload_to="figures/", blank=True)
    is_heroine = models.BooleanField("Eroína nasionál", default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Figura"
        verbose_name_plural = "Figura sira"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:170]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SecretaryGeneralMandate(TranslatedMixin, SampleFlag, models.Model):
    """Historic list of OPMT Secretaries-General."""

    number = models.PositiveIntegerField("Númeru (dahuluk, daruak…)")
    name = models.CharField(max_length=150)
    nickname = models.CharField(max_length=80, blank=True)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(null=True, blank=True)
    figure = models.ForeignKey(Figure, null=True, blank=True, on_delete=models.SET_NULL)
    add_translated(locals(), "note", kind="text")
    photo = models.ImageField(upload_to="leaders/", blank=True)

    class Meta:
        ordering = ["number"]
        verbose_name = "Mandatu Sekretária-Jeral"
        verbose_name_plural = "Mandatu Sekretária-Jeral sira"

    def __str__(self):
        return f"{self.number}. {self.name}"


class Organ(TranslatedMixin, models.Model):
    """National organs defined in the statutes (Art. 19)."""

    code = models.SlugField(max_length=30, unique=True)
    order = models.PositiveIntegerField(default=0)
    add_translated(locals(), "name", required=True)
    add_translated(locals(), "description", kind="text")

    class Meta:
        ordering = ["order"]
        verbose_name = "Órgaun nasionál"
        verbose_name_plural = "Órgaun nasionál sira"

    def __str__(self):
        return self.name_tet


class Municipality(SampleFlag, models.Model):
    name = models.CharField(max_length=80, unique=True)
    code = models.SlugField(max_length=30, unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    coordinator = models.CharField("Koordenadora munisipál", max_length=150, blank=True)
    phone = models.CharField(max_length=60, blank=True)
    members_count = models.PositiveIntegerField("Membru (estimativa)", default=0)
    sucos_with_structure = models.PositiveIntegerField("Suku ho estrutura", default=0)
    is_special_region = models.BooleanField("RAEOA", default=False)

    class Meta:
        ordering = ["name"]
        verbose_name = "Munisípiu"
        verbose_name_plural = "Munisípiu sira"

    def __str__(self):
        return self.name


class AdministrativePost(models.Model):
    municipality = models.ForeignKey(Municipality, related_name="posts", on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    secretary = models.CharField("Sekretária postu", max_length=150, blank=True)

    class Meta:
        ordering = ["municipality__name", "name"]
        unique_together = ("municipality", "name")
        verbose_name = "Postu administrativu"
        verbose_name_plural = "Postu administrativu sira"

    def __str__(self):
        return f"{self.name} ({self.municipality})"


class Leader(TranslatedMixin, SampleFlag, Timestamped):
    """Current leadership (Secretariado, organs, municipal coordinators)."""

    organ = models.ForeignKey(Organ, null=True, blank=True, on_delete=models.SET_NULL, related_name="leaders")
    municipality = models.ForeignKey(Municipality, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=150)
    add_translated(locals(), "position", required=True)
    add_translated(locals(), "bio", kind="text")
    photo = models.ImageField(upload_to="leaders/", blank=True)
    term_start = models.PositiveIntegerField(null=True, blank=True)
    term_end = models.PositiveIntegerField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Lideransa"
        verbose_name_plural = "Lideransa atuál"

    def __str__(self):
        return f"{self.name} – {self.position_tet}"


class Activity(TranslatedMixin, SampleFlag, Timestamped):
    CATEGORY = [
        ("training", "Formasaun"),
        ("advocacy", "Advokasia"),
        ("socioeconomic", "Sósiu-ekonómiku"),
        ("commemoration", "Komemorasaun"),
        ("organisation", "Organizasaun"),
        ("publication", "Publikasaun"),
    ]
    STATUS = [("planned", "Planeadu"), ("ongoing", "Hala'o hela"), ("done", "Remata")]
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY, default="organisation")
    status = models.CharField(max_length=10, choices=STATUS, default="done")
    add_translated(locals(), "title", required=True)
    add_translated(locals(), "summary", kind="text")
    add_translated(locals(), "body", kind="text")
    date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=150, blank=True)
    municipality = models.ForeignKey(Municipality, null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to="activities/", blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date", "-created_at"]
        verbose_name = "Atividade"
        verbose_name_plural = "Atividade sira"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(Activity, self.title_tet)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title_tet


class Program(TranslatedMixin, models.Model):
    """Ongoing sub-programmes."""

    STATUS = Activity.STATUS
    status = models.CharField(max_length=10, choices=STATUS, default="ongoing")
    order = models.PositiveIntegerField(default=0)
    add_translated(locals(), "title", required=True)
    add_translated(locals(), "description", kind="text")

    class Meta:
        ordering = ["order"]
        verbose_name = "Programa"
        verbose_name_plural = "Programa sira"

    def __str__(self):
        return self.title_tet


class News(TranslatedMixin, SampleFlag, Timestamped):
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    add_translated(locals(), "title", required=True)
    add_translated(locals(), "excerpt", kind="text")
    add_translated(locals(), "body", kind="text")
    published_at = models.DateField()
    image = models.ImageField(upload_to="news/", blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        verbose_name = "Notísia"
        verbose_name_plural = "Notísia sira"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(News, self.title_tet)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title_tet


class Album(TranslatedMixin, Timestamped):
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    add_translated(locals(), "title", required=True)
    date = models.DateField(null=True, blank=True)
    activity = models.ForeignKey(Activity, null=True, blank=True, on_delete=models.SET_NULL)
    cover = models.ImageField(upload_to="gallery/covers/", blank=True)

    class Meta:
        ordering = ["-date", "-created_at"]
        verbose_name = "Álbun"
        verbose_name_plural = "Álbun sira"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(Album, self.title_tet)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title_tet


class Photo(TranslatedMixin, models.Model):
    album = models.ForeignKey(Album, related_name="photos", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="gallery/")
    add_translated(locals(), "caption", required=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Foto"
        verbose_name_plural = "Foto sira"

    def __str__(self):
        return self.caption_tet or f"Foto {self.pk}"


class Document(TranslatedMixin, Timestamped):
    CATEGORY = [
        ("statute", "Estatutu"),
        ("program", "Programa"),
        ("publication", "Publikasaun"),
        ("report", "Relatóriu"),
        ("other", "Seluk"),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY, default="other")
    add_translated(locals(), "title", required=True)
    add_translated(locals(), "description", kind="text")
    year = models.PositiveIntegerField(null=True, blank=True)
    language = models.CharField(max_length=20, blank=True, help_text="Lian dokumentu original (ez. Português)")
    file = models.FileField(upload_to="documents/", blank=True)
    external_url = models.URLField(blank=True)
    is_public = models.BooleanField(default=True, help_text="Se la marka, membru deit mak bele hetan.")

    class Meta:
        ordering = ["-year", "category"]
        verbose_name = "Dokumentu"
        verbose_name_plural = "Dokumentu sira"

    def __str__(self):
        return self.title_tet


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=60, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Mensajen"
        verbose_name_plural = "Mensajen sira"

    def __str__(self):
        return f"{self.name}: {self.subject}"


def unique_slug(model, text):
    base = slugify(text)[:180] or "item"
    slug, n = base, 2
    while model.objects.filter(slug=slug).exists():
        slug = f"{base}-{n}"
        n += 1
    return slug
