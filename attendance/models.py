# attendance/models.py

from django.db import models
from django.utils import timezone
from datetime import time
from employees.models import Employee


class Attendance(models.Model):

    # ================= BASIC =================

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="attendances"
    )

    date = models.DateField(
        default=timezone.localdate
    )

    check_in = models.DateTimeField(
        null=True,
        blank=True
    )

    check_out = models.DateTimeField(
        null=True,
        blank=True
    )

    # ================= STATUS =================

    STATUS_CHOICES = [
        ("PRESENT", "Present"),
        ("ABSENT", "Absent"),
        ("LEAVE", "On Leave"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PRESENT"
    )

    # ================= CALCULATED =================

    working_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    lop_days = models.IntegerField(
        default=0
    )

    is_late = models.BooleanField(
        default=False
    )

    is_half_day = models.BooleanField(
        default=False
    )

    # ================= OFFICE RULES =================

    OFFICE_START = time(9, 0)
    OFFICE_END = time(17, 0)

    HALF_DAY_HOURS = 4

    class Meta:
        unique_together = (
            "employee",
            "date"
        )

        ordering = [
            "-date"
        ]

    def save(self, *args, **kwargs):

        # late entry

        if self.check_in:
            check_time = timezone.localtime(
                self.check_in
            ).time()

            self.is_late = (
                check_time > self.OFFICE_START
            )

        # working hours

        if self.check_in and self.check_out:

            delta = (
                self.check_out -
                self.check_in
            )

            hours = round(
                delta.total_seconds() / 3600,
                2
            )

            self.working_hours = hours

            self.is_half_day = (
                hours <
                self.HALF_DAY_HOURS
            )

            if self.is_half_day:
                self.lop_days = 1
            else:
                self.lop_days = 0

        else:
            self.working_hours = 0
            self.is_half_day = False
            self.lop_days = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.employee.name} | "
            f"{self.date} | "
            f"{self.status}"
        )