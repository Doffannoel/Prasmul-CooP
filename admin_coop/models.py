from userauths.models import CustomUser
from django.db import models

class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='admin_profile')
    full_name = models.CharField(max_length=255)
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female')],
        blank=True
    )
    staff_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.full_name