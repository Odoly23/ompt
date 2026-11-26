from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from accounts import views as acc
from content import views as v

router = DefaultRouter()
router.register("objectives", v.ObjectiveViewSet)
router.register("history", v.HistoryEventViewSet)
router.register("figures", v.FigureViewSet)
router.register("secretaries-general", v.MandateViewSet)
router.register("organs", v.OrganViewSet)
router.register("leaders", v.LeaderViewSet)
router.register("municipalities", v.MunicipalityViewSet)
router.register("activities", v.ActivityViewSet)
router.register("programs", v.ProgramViewSet)
router.register("news", v.NewsViewSet)
router.register("albums", v.AlbumViewSet)
router.register("documents", v.DocumentViewSet)

api = [
    path("site/", v.site_view, name="site"),
    path("stats/", v.stats_view, name="stats"),
    path("contact/", v.contact_view, name="contact"),
    path("auth/login/", acc.LoginView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("auth/logout/", acc.LogoutView.as_view(), name="logout"),
    path("auth/register/", acc.RegisterView.as_view(), name="register"),
    path("auth/me/", acc.MeView.as_view(), name="me"),
    path("auth/change-password/", acc.ChangePasswordView.as_view(), name="change_password"),
    path("auth/member-card/", acc.MemberCardView.as_view(), name="member_card"),
    path("", include(router.urls)),
]

urlpatterns = [
    path("api/v1/", include((api, "api"))),
    path("panel/", include("panel.urls")),
    path("django-admin/", admin.site.urls),
    path("", RedirectView.as_view(url="/panel/", permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
