from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = "panel"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="panel:login"), name="logout"),
    path("settings/", views.site_settings, name="settings"),
    path("members/<int:pk>/<str:action>/", views.member_status, name="member_status"),
    path("<str:key>/", views.object_list, name="list"),
    path("<str:key>/add/", views.object_edit, name="add"),
    path("<str:key>/<int:pk>/", views.object_edit, name="edit"),
    path("<str:key>/<int:pk>/delete/", views.object_delete, name="delete"),
]
