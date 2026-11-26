import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def fill_tokens(apps, schema_editor):
    MemberProfile = apps.get_model("accounts", "MemberProfile")
    for m in MemberProfile.objects.filter(card_token__isnull=True):
        m.card_token = uuid.uuid4()
        m.save(update_fields=["card_token"])


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
        ("content", "0003_slides"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="memberprofile",
            name="card_token",
            field=models.UUIDField(null=True, editable=False),
        ),
        migrations.RunPython(fill_tokens, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="memberprofile",
            name="card_token",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.CreateModel(
            name="StaffProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(blank=True, max_length=120, verbose_name="Knaar")),
                ("phone", models.CharField(blank=True, max_length=60)),
                ("municipality", models.ForeignKey(blank=True, help_text="Mamuk = ekipa nasionál (asesu tomak)", null=True, on_delete=django.db.models.deletion.PROTECT, to="content.municipality")),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="staff_profile", to=settings.AUTH_USER_MODEL)),
            ],
            options={"verbose_name": "Ekipa panel", "verbose_name_plural": "Ekipa panel"},
        ),
    ]
