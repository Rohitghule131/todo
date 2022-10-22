from django.db import models
from django.utils import timezone
from user.models import CustomUser


class ToDoTaskModel(models.Model):
    priorities = {
        ("HIGH", "HIGH"),
        ("MEDIUM", "MEDIUM"),
        ("LOW", "LOW")
    }
    status = {
        ("PENDING", "PENDING"),
        ("COMPLETED", "COMPLETED"),
        ("ONGOING", "ONGOING")
    }
    user = models.ForeignKey(CustomUser, verbose_name="User to created task", on_delete=models.CASCADE)
    task = models.CharField(verbose_name="Task", max_length=300, null=False, blank=False)
    priority_level = models.CharField(
        verbose_name="Priority Levels",
        max_length=20,
        choices=priorities,
        null=False,
        blank=False
    )
    status = models.CharField(
        verbose_name="Task Status",
        max_length=20,
        choices=status,
        default="PENDING",
        null=False,
        blank=False
    )
    estimated_time = models.TimeField(
        verbose_name="Estimated Time",
        auto_created=False,
        auto_now=False,
        auto_now_add=False
    )
    task_complete_time = models.TimeField(
        verbose_name="Time for complete the task",
        null=False,
        blank=False,
        default="00:00"
    )
    start_date_of_task = models.DateTimeField(
        verbose_name="Task start date and time",
        null=False,
        blank=False,
    )
    end_date_of_task = models.DateTimeField(
        verbose_name="Task end date and time",
        null=False,
        blank=False,
    )
    created_at = models.DateTimeField(
        verbose_name="Task created date and time",
        null=False,
        blank=False,
        default=timezone.now()
    )
