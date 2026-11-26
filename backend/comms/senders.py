"""Delivery of announcements by email and SMS.

Email uses Django's email settings (SMTP in production, console in development).
SMS uses SMS_BACKEND:
  - "console": print messages to the server log (default; nothing is sent)
  - "http":    POST to an SMS gateway (e.g. Telkomcel / Timor Telecom / Telemor bulk SMS API)
               configured with SMS_HTTP_URL, SMS_HTTP_TOKEN, SMS_HTTP_TO_FIELD, SMS_HTTP_TEXT_FIELD,
               SMS_HTTP_SENDER_FIELD and SMS_SENDER_ID.
"""
import json
import logging
import urllib.request

from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.utils import timezone

log = logging.getLogger("opmt.comms")
SMS_MAX = 300


def normalise_phone(phone):
    digits = "".join(ch for ch in (phone or "") if ch.isdigit() or ch == "+")
    if not digits:
        return ""
    if digits.startswith("+"):
        return digits
    if digits.startswith("670"):
        return "+" + digits
    return "+670" + digits.lstrip("0")


def send_sms(phone, text):
    to = normalise_phone(phone)
    if not to:
        return False
    text = text[:SMS_MAX]
    backend = getattr(settings, "SMS_BACKEND", "console")
    if backend == "console":
        log.warning("SMS (console) to %s: %s", to, text)
        print(f"[SMS console] {to}: {text}")
        return True
    if backend == "http":
        payload = {
            settings.SMS_HTTP_TO_FIELD: to,
            settings.SMS_HTTP_TEXT_FIELD: text,
        }
        if settings.SMS_SENDER_ID:
            payload[settings.SMS_HTTP_SENDER_FIELD] = settings.SMS_SENDER_ID
        req = urllib.request.Request(
            settings.SMS_HTTP_URL, data=json.dumps(payload).encode(), method="POST",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {settings.SMS_HTTP_TOKEN}"},
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return 200 <= resp.status < 300
        except Exception as exc:  # gateway down, bad number…
            log.error("SMS to %s failed: %s", to, exc)
            return False
    raise ValueError(f"Unknown SMS_BACKEND {backend!r}")


def send_announcement(announcement, user=None):
    members = list(announcement.recipients())
    want_email = announcement.channel in ("email", "email_sms")
    want_sms = announcement.channel in ("sms", "email_sms")
    email_ok = sms_ok = failures = 0

    if want_email:
        connection = get_connection(fail_silently=False)
        subject = f"OPMT: {announcement.title}"
        for m in members:
            if not m.user.email:
                continue
            try:
                EmailMessage(subject, announcement.body, settings.DEFAULT_FROM_EMAIL, [m.user.email], connection=connection).send()
                email_ok += 1
            except Exception as exc:
                log.error("Email to %s failed: %s", m.user.email, exc)
                failures += 1

    if want_sms:
        text = f"OPMT: {announcement.title}. {announcement.body}"
        for m in members:
            if send_sms(m.phone, text):
                sms_ok += 1
            else:
                failures += 1

    announcement.status = "sent"
    announcement.sent_at = timezone.now()
    announcement.sent_by = user
    announcement.recipients_count = len(members)
    announcement.email_sent = email_ok
    announcement.sms_sent = sms_ok
    announcement.failures = failures
    announcement.save()
    return announcement
