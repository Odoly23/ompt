"""Load the initial OPMT content.

    python manage.py seed_opmt            # create content if the database is empty
    python manage.py seed_opmt --reset    # delete content (not members) and reload
    python manage.py seed_opmt --admin admin@opmt.tl   # also create a staff user
"""
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from content import seed_data as D
from content.models import (
    Activity, AdministrativePost, Album, Document, Figure, HistoryEvent, Leader, Municipality,
    News, Objective, Organ, Photo, Program, SecretaryGeneralMandate, SiteSetting, Slide,
)

FILES = Path(__file__).resolve().parents[2] / "seed_files"


def tr(prefix, values):
    return {f"{prefix}_{lang}": text for lang, text in values.items()}


def attach(field, filename):
    path = FILES / filename
    if path.exists():
        with path.open("rb") as fh:
            field.save(filename, File(fh), save=False)


class Command(BaseCommand):
    help = "Load initial OPMT website content (history, figures, organs, municipalities…)."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Delete existing content first")
        parser.add_argument("--admin", help="Create a staff user with this email (password asked or OPMT_ADMIN_PASSWORD)")

    @transaction.atomic
    def handle(self, *args, **opts):
        if opts["reset"]:
            for model in (Slide, Photo, Album, Activity, News, Document, Leader, AdministrativePost,
                          SecretaryGeneralMandate, Figure, HistoryEvent, Objective, Program, Organ):
                model.objects.all().delete()
            Municipality.objects.filter(memberprofile__isnull=True).delete()
        elif HistoryEvent.objects.exists():
            self.seed_slides()
            self.stdout.write("Content already loaded. Use --reset to reload.")
            return self.create_admin(opts.get("admin"))

        site = SiteSetting.load()
        site.name = D.SITE["name"]
        site.short_name = D.SITE["short_name"]
        site.founded = D.SITE["founded"]
        site.address = D.SITE["address"]
        for key in ("tagline", "about", "mission"):
            for k, v in tr(key, D.SITE[key]).items():
                setattr(site, k, v)
        if not site.logo:
            attach(site.logo, "opmt-logo.jpg")
        site.save()

        general = Objective(kind="general", order=0, **tr("text", D.SITE["mission"]))
        general.save()
        for i, o in enumerate(D.OBJECTIVES, 1):
            Objective.objects.create(kind=o["kind"], order=i, **tr("text", o["text"]))

        for i, h in enumerate(D.HISTORY):
            HistoryEvent.objects.create(
                year=h["year"], date=h.get("date"), category=h["category"], order=i,
                **tr("title", h["title"]), **tr("body", h["body"]),
            )

        figures = {}
        for f in D.FIGURES:
            obj = Figure.objects.create(
                name=f["name"], nickname=f.get("nickname", ""), death_year=f.get("death_year"),
                birth_year=f.get("birth_year"), is_heroine=f.get("is_heroine", False), order=f["order"],
                **tr("role", f["role"]), **tr("bio", f["bio"]),
            )
            figures[f["name"]] = obj

        for m in D.MANDATES:
            SecretaryGeneralMandate.objects.create(
                number=m["number"], name=m["name"], nickname=m.get("nickname", ""),
                start_year=m["start_year"], end_year=m.get("end_year"),
                figure=figures.get(m.get("figure")), **tr("note", m["note"]),
            )

        organs = {}
        for o in D.ORGANS:
            organs[o["code"]] = Organ.objects.create(
                code=o["code"], order=o["order"], **tr("name", o["name"]), **tr("description", o["description"]),
            )

        for l in D.LEADERS:
            Leader.objects.create(
                organ=organs[l["organ"]], name=l["name"], order=l["order"], is_sample=True,
                **tr("position", l["position"]),
            )

        munis = {}
        for name, code, lat, lng, special in D.MUNICIPALITIES:
            munis[code], _ = Municipality.objects.update_or_create(
                code=code,
                defaults=dict(name=name, latitude=lat, longitude=lng, is_special_region=special, is_sample=True),
            )
        for code, posts in D.POSTS.items():
            for p in posts:
                AdministrativePost.objects.get_or_create(municipality=munis[code], name=p)

        for p in D.PROGRAMS:
            Program.objects.create(order=p["order"], status="ongoing", **tr("title", p["title"]), **tr("description", p["description"]))

        poster_activity = None
        for a in D.ACTIVITIES:
            act = Activity(
                category=a["category"], status=a["status"], date=a.get("date"), location=a.get("location", ""),
                municipality=munis.get(a.get("municipality")), is_sample=a.get("sample", False),
                **tr("title", a["title"]), **tr("summary", a["summary"]), **tr("body", a["body"]),
            )
            if "Espozisaun" in a["title"]["tet"]:
                attach(act.image, "buibere-hamrik-poster.jpg")
                poster_activity = act
            act.save()

        for n in D.NEWS:
            News.objects.create(
                published_at=n["published_at"], **tr("title", n["title"]),
                **tr("excerpt", n["excerpt"]), **tr("body", n["body"]),
            )

        for d in D.DOCUMENTS:
            doc = Document(category=d["category"], year=d["year"], language=d["language"],
                           **tr("title", d["title"]), **tr("description", d["description"]))
            attach(doc.file, d["file"])
            doc.save()

        album = Album(
            date="2016-02-25", activity=poster_activity,
            **tr("title", {"tet": "Espozisaun Buibere Hamrik", "pt": "Exposição Buibere Hamrik",
                           "id": "Pameran Buibere Hamrik", "en": "Buibere Hamrik exhibition"}),
        )
        attach(album.cover, "buibere-hamrik-poster.jpg")
        album.save()
        photo = Photo(album=album, **tr("caption", {
            "tet": "Kapa espozisaun \"Buibere Hamrik Tuba Rai Metin Ukun Rasik An\"",
            "pt": "Capa da exposição \"Buibere Hamrik Tuba Rai Metin Ukun Rasik An\"",
            "id": "Sampul pameran \"Buibere Hamrik Tuba Rai Metin Ukun Rasik An\"",
            "en": "Cover of the \"Buibere Hamrik Tuba Rai Metin Ukun Rasik An\" exhibition"}))
        attach(photo.image, "buibere-hamrik-poster.jpg")
        photo.save()

        self.seed_slides()
        self.stdout.write(self.style.SUCCESS("OPMT content loaded."))
        self.create_admin(opts.get("admin"))

    def seed_slides(self):
        if Slide.objects.exists():
            return
        for i, sl in enumerate(D.SLIDES, 1):
            slide = Slide(order=i, theme=sl["theme"], link=sl.get("link", ""),
                          **tr("title", sl["title"]), **tr("text", sl["text"]), **tr("button", sl["button"]))
            if sl.get("image"):
                attach(slide.image, sl["image"])
            slide.save()
        self.stdout.write("Slides loaded.")

    def create_admin(self, email):
        if not email:
            return
        import os
        from getpass import getpass

        User = get_user_model()
        if User.objects.filter(username=email).exists():
            self.stdout.write(f"User {email} already exists.")
            return
        password = os.getenv("OPMT_ADMIN_PASSWORD") or getpass("Password for the admin user: ")
        User.objects.create_superuser(username=email, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Admin {email} created."))
