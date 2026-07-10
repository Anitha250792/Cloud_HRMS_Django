from django.urls import path
from .views import (
    EmployeeListView,
    AddEmployeeView,
    EditEmployeeView,
    DeleteEmployeeView
)

urlpatterns = [

    # default page
    path(
        "",
        EmployeeListView.as_view(),
        name="employees"
    ),

    path(
        "list/",
        EmployeeListView.as_view(),
        name="employee_list"
    ),

    path(
        "add/",
        AddEmployeeView.as_view(),
        name="add_employee"
    ),

    path(
        "edit/<int:pk>/",
        EditEmployeeView.as_view(),
        name="edit_employee"
    ),

    path(
        "delete/<int:pk>/",
        DeleteEmployeeView.as_view(),
        name="delete_employee"
    ),
]