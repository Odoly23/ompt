from django.contrib.auth.views import LogoutView
from django.urls import path

from . import reports, views

app_name = "panel"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="panel:login"), name="logout"),
    path("settings/", views.site_settings, name="settings"),
    path("stats/", reports.stats, name="stats"),
    path("dues-report/", reports.dues_report, name="dues_report"),
    path("scan/", views.scan, name="scan"),
    path("scan/check/", views.scan_check, name="scan_check"),
    path("team/", views.team, name="team"),
    path("team/<int:pk>/toggle/", views.team_toggle, name="team_toggle"),
    path("export/members.xlsx", reports.export_members, name="export_members"),
    path("export/payments.xlsx", reports.export_payments, name="export_payments"),
    path("export/event/<int:event_id>.xlsx", reports.export_registrations, name="export_registrations"),
    path("announcements/<int:pk>/send/", views.announcement_send, name="announcement_send"),
    path("registrations/<int:pk>/checkin/", views.registration_checkin, name="registration_checkin"),
    path("members/<int:pk>/<str:action>/", views.member_status, name="member_status"),
    path("<str:key>/", views.object_list, name="list"),
    path("<str:key>/add/", views.object_edit, name="add"),
    path("<str:key>/<int:pk>/", views.object_edit, name="edit"),
    path("<str:key>/<int:pk>/delete/", views.object_delete, name="delete"),
]
