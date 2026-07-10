from django.urls import path
from .views import (dashboard_stats, HRDashboardView)

urlpatterns = [
    path(
        "api/stats/",
        dashboard_stats,
        name="dashboard_stats"
    ),

    path(
        "",
        HRDashboardView.as_view(),
        name="dashboard"
    ),
]