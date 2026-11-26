from django.conf import settings
from django.db import models

from content.models import Municipality


class Announcement(models.Model):
    """A message to members: shown in their dashboard, and optionally sent by email/SMS."""

    CHANNELS = [("site", "Website deit"), ("email", "Email"), ("sms", "SMS"), ("email_sms", "Email + SMS")]
    STATUS = [("draft", "Rascunhu"), ("sent", "Haruka ona")]
    AUDIENCE = [("active", "Membru ativu"), ("all", "Membru hotu (inklui hein aprovasaun)")]

    title = models.CharField(max_length=200)
    body = models.TextField(help_text="SMS sei uza karakter 300 dahuluk deit.")
    channel = models.CharField(max_length=10, choices=CHANNELS, default="site")
    audience = models.CharField(max_length=10, choices=AUDIENCE, default="active")
    municipality = models.ForeignKey(Municipality, null=True, blank=True, on_delete=models.SET_NULL, help_text="Mamuk = nasionál")
    status = models.CharField(max_length=10, choices=STATUS, default="draft")
    sent_at = models.DateTimeField(null=True, blank=True)
    sent_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    recipients_count = models.PositiveIntegerField(default=0)
    email_sent = models.PositiveIntegerField(default=0)
    sms_sent = models.PositiveIntegerField(default=0)
    failures = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Anúnsiu"
        verbose_name_plural = "Anúnsiu sira"

    def __str__(self):
        return self.title

    def recipients(self):
        from accounts.models import MemberProfile

        qs = MemberProfile.objects.select_related("user")
        qs = qs.filter(status="active") if self.audience == "active" else qs.exclude(status__in=["rejected", "inactive"])
        if self.municipality_id:
            qs = qs.filter(municipality_id=self.municipality_id)
        return qs
