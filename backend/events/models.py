from django.conf import settings
from django.db import models
from django.utils import timezone

from content.i18n import TranslatedMixin, add_translated
from content.models import Municipality, Timestamped, unique_slug


class Event(TranslatedMixin, Timestamped):
    """An agenda item members and the public can register for."""

    slug = models.SlugField(max_length=200, unique=True, blank=True)
    add_translated(locals(), "title", required=True)
    add_translated(locals(), "description", kind="text")
    starts_at = models.DateTimeField()
    time_confirmed = models.BooleanField("Oras konfirma ona", default=True, help_text="Se la marka, website hatudu data deit, la hatudu oras.")
    ends_at = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    municipality = models.ForeignKey(Municipality, null=True, blank=True, on_delete=models.SET_NULL)
    capacity = models.PositiveIntegerField(null=True, blank=True, help_text="Mamuk = la iha limite")
    registration_open = models.BooleanField(default=True)
    members_only = models.BooleanField(default=False, help_text="Membru ativu deit mak bele rejista")
    image = models.ImageField(upload_to="events/", blank=True)
    is_published = models.BooleanField(default=True)
    is_sample = models.BooleanField("Dadus ezemplu", default=False)

    class Meta:
        ordering = ["starts_at"]
        verbose_name = "Eventu"
        verbose_name_plural = "Agenda (eventu sira)"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(Event, self.title_tet)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.starts_at:%d/%m/%Y} – {self.title_tet}"

    @property
    def is_past(self):
        return (self.ends_at or self.starts_at) < timezone.now()

    @property
    def registered_count(self):
        return self.registrations.exclude(status="cancelled").count()

    @property
    def spots_left(self):
        if self.capacity is None:
            return None
        return max(0, self.capacity - self.registered_count)


class Registration(models.Model):
    STATUS = [("registered", "Rejista ona"), ("attended", "Mai ona"), ("cancelled", "Kansela")]
    event = models.ForeignKey(Event, related_name="registrations", on_delete=models.CASCADE)
    member = models.ForeignKey("accounts.MemberProfile", null=True, blank=True, on_delete=models.CASCADE, related_name="registrations")
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=60, blank=True)
    email = models.EmailField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS, default="registered")
    checked_in_at = models.DateTimeField(null=True, blank=True)
    checked_in_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Rejistu partisipante"
        verbose_name_plural = "Rejistu partisipante sira"
        constraints = [
            models.UniqueConstraint(fields=["event", "member"], condition=models.Q(member__isnull=False), name="one_registration_per_member"),
        ]

    def __str__(self):
        return f"{self.name} → {self.event.title_tet}"

    def check_in(self, user=None):
        self.status = "attended"
        self.checked_in_at = timezone.now()
        self.checked_in_by = user
        self.save(update_fields=["status", "checked_in_at", "checked_in_by"])
