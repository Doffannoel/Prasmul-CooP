from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.pop('username', None)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email, password, and admin privileges."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = None  # Hapus field username bawaan Django
    USERNAME_FIELD = 'email'  # Gunakan email sebagai login
    REQUIRED_FIELDS = []  # Hapus username dari required fields
    is_admin_coop = models.BooleanField(default=False)  # Menandai sebagai Admin Co-op
    is_student = models.BooleanField(default=False)  # Menandai sebagai Mahasiswa

    objects = CustomUserManager()  # Gunakan custom manager

    def __str__(self):
        return self.email
