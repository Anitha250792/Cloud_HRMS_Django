from django.urls import path
from . import views

urlpatterns = [

    path(
        "hr/login/",
        views.hr_login,
        name="hr_login"
    ),

    path(
        "employee/login/",
        views.employee_login,
        name="employee_login"
    ),
]