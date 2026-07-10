from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):

    sender = models.ForeignKey(
        User,
        related_name='sent_notifications',
        on_delete=models.CASCADE
    )

    receiver = models.ForeignKey(
        User,
        related_name='notifications',
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    message = models.TextField()

    category = models.CharField(
        max_length=30,
        choices=[
            ("LEAVE","LEAVE"),
            ("PAYROLL","PAYROLL"),
            ("ATTENDANCE","ATTENDANCE"),
            ("SYSTEM","SYSTEM")
        ]
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering=['-created_at']