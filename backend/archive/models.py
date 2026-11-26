from django.db import models

from content.models import Municipality, Timestamped, unique_slug


class Story(Timestamped):
    """Memória Buibere: testimonies of women in the struggle.

    Stories are kept in the language they were told in (not translated), and
    public submissions wait for moderation before they are published.
    """

    ERA = [
        ("1975", "1975 – Fundasaun no invazaun"),
        ("resistance", "1975–1999 – Rezisténsia"),
        ("referendum", "1999 – Referendu"),
        ("independence", "2002 – ohin – Independénsia"),
    ]
    FRONT = [
        ("armed", "Frente armada"),
        ("clandestine", "Frente klandestina"),
        ("diplomatic", "Frente diplomátika / esterna"),
        ("community", "Komunidade / Bases de Apoio"),
        ("other", "Seluk"),
    ]
    STATUS = [("pending", "Hein moderasaun"), ("published", "Publika ona"), ("rejected", "Rejeita")]
    LANG = [("tet", "Tetun"), ("pt", "Português"), ("id", "Indonesia"), ("en", "English"), ("other", "Lian seluk")]

    slug = models.SlugField(max_length=200, unique=True, blank=True)
    title = models.CharField(max_length=200)
    storyteller = models.CharField("Na'in ba istória", max_length=150)
    nickname = models.CharField(max_length=80, blank=True)
    municipality = models.ForeignKey(Municipality, null=True, blank=True, on_delete=models.SET_NULL)
    era = models.CharField(max_length=20, choices=ERA, default="resistance")
    front = models.CharField(max_length=20, choices=FRONT, default="community")
    language = models.CharField(max_length=10, choices=LANG, default="tet")
    summary = models.CharField(max_length=300, blank=True)
    body = models.TextField()
    photo = models.ImageField(upload_to="memoria/photos/", blank=True)
    audio = models.FileField(upload_to="memoria/audio/", blank=True, help_text="mp3, m4a, ogg")
    video_url = models.URLField(blank=True, help_text="YouTube ka Facebook")
    status = models.CharField(max_length=10, choices=STATUS, default="pending")
    is_featured = models.BooleanField(default=False)
    is_sample = models.BooleanField("Dadus ezemplu", default=False)
    # Who sent it (not shown publicly)
    submitted_by = models.CharField(max_length=150, blank=True)
    submitter_contact = models.CharField(max_length=150, blank=True)
    consent = models.BooleanField("Na'in ba istória fó lisensa", default=False)
    moderation_note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-is_featured", "-created_at"]
        verbose_name = "Istória Memória Buibere"
        verbose_name_plural = "Memória Buibere"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(Story, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
