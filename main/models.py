from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class RoadDamageReport(models.Model):
    SEVERITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Resolved", "Resolved"),
    ]

    reporter_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    location = models.CharField(max_length=200)
    road_name = models.CharField(max_length=200)
    damage_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default="Medium")
    description = models.TextField()
    photo = models.ImageField(upload_to="complaints/", blank=True, null=True)
    reported_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return f"{self.reporter_name} - {self.road_name}"
