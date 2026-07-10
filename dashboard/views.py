from rest_framework.decorators import (
    api_view,
    permission_classes
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.views.generic import TemplateView
from django.utils import timezone

from employees.models import Employee
from leave.models import Leave
from payroll.models import Payroll


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):

    today = timezone.localdate()

    employees = Employee.objects.filter(
        is_active=True
    ).count()

    pending_leaves = Leave.objects.filter(
        status="PENDING"
    ).count()

    approved_leaves = Leave.objects.filter(
        status="APPROVED"
    ).count()

    rejected_leaves = Leave.objects.filter(
        status="REJECTED"
    ).count()

    generated_payslips = Payroll.objects.filter(
        month=today.month,
        year=today.year
    ).count()

    return Response({
        "employees": employees,
        "pending_leaves": pending_leaves,
        "approved_leaves": approved_leaves,
        "rejected_leaves": rejected_leaves,
        "generated_payslips": generated_payslips
    })


class HRDashboardView(TemplateView):

    template_name = "dashboard/hr_dashboard.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        today = timezone.localdate()

        employee_count = Employee.objects.filter(
            is_active=True
        ).count()

        generated_count = Payroll.objects.filter(
            month=today.month,
            year=today.year
        ).count()

        pending_count = Leave.objects.filter(
            status="PENDING"
        ).count()

        progress = 0

        if employee_count > 0:
            progress = round(
                (generated_count / employee_count) * 100
            )

        context.update({

            "employee_count": employee_count,

            "generated_count": generated_count,

            "pending_count": pending_count,

            "progress": progress,

            "last_generation":
                today.strftime("%b %d"),

            "batch_id":
                f"PS-{today.year}{today.month:02}",
        })

        return context


class EmployeeProfileView(TemplateView):

    template_name = "employee/profile.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        try:
            context["employee"] = Employee.objects.get(
                user=self.request.user
            )
        except Employee.DoesNotExist:
            context["employee"] = None

        return context