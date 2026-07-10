from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from .views import RoleRedirectView, admin_dashboard_stats, health_check
from accounts.views import RegisterView, LoginView
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import login_page


urlpatterns = [
    path("health/", health_check),
    path("", login_page),
    path("", RoleRedirectView.as_view()),
    path("admin/", admin.site.urls),

    path("", include("accounts.urls")),

    # Dashboard
    path(
        "api/dashboard/",
        include("dashboard.urls")
    ),

    # Employee Templates
    path(
        "employees/",
        include("employees.urls")
    ),

    # APIs
    path(
        "api/employees/",
        include("employees.urls")
    ),
    path(
        "api/attendance/",
        include("attendance.urls")
    ),
    path(
        "api/payroll/",
        include("payroll.urls")
    ),
    path(
        "api/leave/",
        include("leave.urls")
    ),

    path(
        "",
        include("authentication.urls")
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )