from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.contrib.auth import get_user_model
from django.contrib import messages

from .models import Employee
from django.db.models import Q

User = get_user_model()


# ==================================================
# EMPLOYEE LIST
# ==================================================


class EmployeeListView(TemplateView):

    template_name = "hr/employees/employee_list.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        employees = Employee.objects.all().order_by("-id")

        search = self.request.GET.get("search")
        department = self.request.GET.get("department")
        status = self.request.GET.get("status")

        if search:
            employees = employees.filter(
                Q(name__icontains=search)
                |
                Q(emp_code__icontains=search)
            )

        if department:
            employees = employees.filter(
                department=department
            )

        if status == "active":
            employees = employees.filter(
                is_active=True
            )

        elif status == "inactive":
            employees = employees.filter(
                is_active=False
            )

        context["employees"] = employees

        context["departments"] = (
            Employee.objects
            .values_list(
                "department",
                flat=True
            )
            .distinct()
        )

        return context


# ==================================================
# ADD EMPLOYEE
# ==================================================

class AddEmployeeView(View):

    template_name = "hr/employees/add_employee.html"

    def get(self, request):

        return render(
            request,
            self.template_name
        )

    def post(self, request):

        try:

            email = request.POST.get("email")
            emp_code = request.POST.get("emp_code")

            # prevent duplicate employee code
            if Employee.objects.filter(
                emp_code=emp_code
            ).exists():

                messages.error(
                    request,
                    "Employee code already exists"
                )

                return redirect(
                    "add_employee"
                )

            # prevent duplicate email
            if Employee.objects.filter(
                email=email
            ).exists():

                messages.error(
                    request,
                    "Email already exists"
                )

                return redirect(
                    "add_employee"
                )

            user, created = User.objects.get_or_create(

                email=email,

                defaults={
                    "name":
                        request.POST.get("name"),
                    "role":
                        "EMPLOYEE",
                }
            )

            if created:

                user.set_password(
                    "Default@123"
                )

                user.save()

            status = (
    request.POST.get("is_active")
    == "true"
)

            Employee.objects.create(

                user=user,

                emp_code=emp_code,

                name=request.POST.get(
                    "name"
                ),

                email=email,

                phone=request.POST.get(
                    "phone"
                ),

                gender=request.POST.get(
                    "gender"
                ),

                dob=request.POST.get(
                    "dob"
                ),

                department=request.POST.get(
                    "department"
                ),

                designation=request.POST.get(
                    "designation"
                ),

                role=request.POST.get(
                    "role"
                ),

                date_joined=request.POST.get(
                    "date_joined"
                ),

                salary=request.POST.get(
                    "salary"
                ),

                bank_name=request.POST.get(
                    "bank_name"
                ),

                bank_account=request.POST.get(
                    "bank_account"
                ),

                ifsc_code=request.POST.get(
                    "ifsc_code"
                ),

                pan_number=request.POST.get(
                    "pan_number"
                ),

                pf_number=request.POST.get(
                    "pf_number"
                ),

                profile_photo=request.FILES.get(
                    "profile_photo"
                ),

                is_active=status,
            )

            messages.success(
                request,
                "Employee added successfully"
            )

            return redirect(
                "employee_list"
            )

        except Exception as e:

            print(
                "ADD ERROR:",
                str(e)
            )

            messages.error(
                request,
                str(e)
            )

            return redirect(
                "add_employee"
            )


# ==================================================
# EDIT EMPLOYEE
# ==================================================

class EditEmployeeView(View):

    template_name = "hr/employees/edit_employee.html"

    def get(self, request, pk):

        employee = get_object_or_404(
            Employee,
            pk=pk
        )

        return render(
            request,
            self.template_name,
            {
                "employee": employee
            }
        )

    def post(self, request, pk):

        try:

            employee = get_object_or_404(
                Employee,
                pk=pk
            )

            employee.emp_code = request.POST.get(
                "emp_code"
            )

            employee.name = request.POST.get(
                "name"
            )

            employee.email = request.POST.get(
                "email"
            )

            employee.phone = request.POST.get(
                "phone"
            )

            employee.gender = request.POST.get(
                "gender"
            )

            employee.department = request.POST.get(
                "department"
            )

            employee.designation = request.POST.get(
                "designation"
            )

            employee.role = request.POST.get(
                "role"
            )

            employee.salary = request.POST.get(
                "salary"
            )

            employee.bank_name = request.POST.get(
                "bank_name"
            )

            employee.bank_account = request.POST.get(
                "bank_account"
            )

            employee.ifsc_code = request.POST.get(
                "ifsc_code"
            )

            employee.pan_number = request.POST.get(
                "pan_number"
            )

            employee.pf_number = request.POST.get(
                "pf_number"
            )

            if request.FILES.get(
                "profile_photo"
            ):

                employee.profile_photo = (
                    request.FILES.get(
                        "profile_photo"
                    )
                )

            employee.is_active = (
    request.POST.get("is_active")
    == "true"
)

            employee.save()

            messages.success(
                request,
                "Employee updated"
            )

            return redirect(
                "employee_list"
            )

        except Exception as e:

            print(
                "EDIT ERROR:",
                str(e)
            )

            messages.error(
                request,
                str(e)
            )

            return redirect(
                "employee_list"
            )


# ==================================================
# DELETE EMPLOYEE
# ==================================================

class DeleteEmployeeView(View):

    def get(self, request, pk):

        employee = get_object_or_404(
            Employee,
            pk=pk
        )

        employee.is_active = False

        employee.save()

        messages.success(
            request,
            "Employee deleted"
        )

        return redirect(
            "employee_list"
        )
    
