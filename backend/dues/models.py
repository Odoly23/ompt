"""Member dues (quotização). Estatutu Art. 22 (j): the National Coordinating
Council approves the dues system and minimum amount every two years."""
from decimal import Decimal

from django.conf import settings
from django.db import models


class DuesRate(models.Model):
    year = models.PositiveIntegerField(unique=True)
    annual_amount = models.DecimalField("Valór tinan ida (USD)", max_digits=8, decimal_places=2)
    note = models.CharField(max_length=255, blank=True, help_text="Ez. desizaun CCN data …")

    class Meta:
        ordering = ["-year"]
        verbose_name = "Valór kuota"
        verbose_name_plural = "Valór kuota sira"

    def __str__(self):
        return f"{self.year}: ${self.annual_amount}"

    @classmethod
    def for_year(cls, year):
        return cls.objects.filter(year__lte=year).order_by("-year").first()


class Payment(models.Model):
    METHOD = [("cash", "Osan kontadu"), ("bank", "Transferénsia banku"), ("mobile", "Mobile money"), ("other", "Seluk")]
    member = models.ForeignKey("accounts.MemberProfile", related_name="payments", on_delete=models.CASCADE)
    year = models.PositiveIntegerField("Tinan kuota")
    amount = models.DecimalField("Montante (USD)", max_digits=8, decimal_places=2)
    paid_on = models.DateField("Data selu")
    method = models.CharField(max_length=10, choices=METHOD, default="cash")
    receipt_number = models.CharField("Númeru resibu", max_length=40, blank=True)
    note = models.CharField(max_length=255, blank=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-paid_on", "-created_at"]
        verbose_name = "Pagamentu kuota"
        verbose_name_plural = "Pagamentu kuota sira"

    def __str__(self):
        return f"{self.member} – {self.year} – ${self.amount}"


def member_balance(member, year):
    """(due, paid, outstanding) for one member and year."""
    rate = DuesRate.for_year(year)
    due = rate.annual_amount if rate else Decimal("0")
    paid = sum((p.amount for p in member.payments.filter(year=year)), Decimal("0"))
    return due, paid, max(Decimal("0"), due - paid)
