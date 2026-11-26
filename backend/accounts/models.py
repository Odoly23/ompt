from datetime import date

from django.conf import settings
from django.db import models

from content.models import AdministrativePost, Municipality


class MemberProfile(models.Model):
    """OPMT membership (Estatutos Art. 6: Timorese woman, 16 years or older)."""

    STATUS = [
        ("pending", "Hein aprovasaun"),
        ("active", "Ativu"),
        ("rejected", "Rejeita"),
        ("inactive", "La ativu"),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="member", on_delete=models.CASCADE)
    member_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=150)
    birth_date = models.DateField()
    phone = models.CharField(max_length=60)
    municipality = models.ForeignKey(Municipality, on_delete=models.PROTECT)
    administrative_post = models.ForeignKey(AdministrativePost, null=True, blank=True, on_delete=models.SET_NULL)
    suco = models.CharField(max_length=80, blank=True)
    aldeia = models.CharField(max_length=80, blank=True)
    occupation = models.CharField(max_length=120, blank=True)
    preferred_language = models.CharField(max_length=3, default="tet")
    photo = models.ImageField(upload_to="members/", blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default="pending")
    status_note = models.CharField(max_length=255, blank=True)
    accepts_statutes = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Membru"
        verbose_name_plural = "Membru sira"

    def __str__(self):
        return self.full_name

    @property
    def age(self):
        today = date.today()
        b = self.birth_date
        return today.year - b.year - ((today.month, today.day) < (b.month, b.day))

    def assign_number(self):
        if self.member_number:
            return
        prefix = (self.municipality.code or "TL")[:3].upper()
        count = MemberProfile.objects.filter(member_number__startswith=f"OPMT-{prefix}-").count() + 1
        self.member_number = f"OPMT-{prefix}-{count:05d}"
