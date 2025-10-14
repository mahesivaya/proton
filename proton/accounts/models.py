from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('reception', 'Reception'),
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('patient', 'Patient'),
        ('pharmacy', 'pharmacy'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)


    # Fix reverse accessor conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.username} ({self.role})"


class Admin(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()
    email = models.EmailField()
    phone_number = models.IntegerField()
    address = models.CharField(max_length=255)
    class Meta:
        managed = True

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.age} {self.email} {self.phone_number} {self.address}"


class Patient(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()
    email = models.EmailField()
    phone_number = models.IntegerField()
    address = models.CharField(max_length=255)
    class Meta:
        managed = True

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.age} {self.email} {self.phone_number} {self.address}"


class Doctor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()
    email = models.EmailField()
    phone_number = models.IntegerField()
    address = models.CharField(max_length=255)
    class Meta:
        managed = True

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.age} {self.email} {self.phone_number} {self.address}"


class Nurse(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()
    email = models.EmailField()
    phone_number = models.IntegerField()
    address = models.CharField(max_length=255)
    class Meta:
        managed = True

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.age} {self.email} {self.phone_number} {self.address}"


class Nurse(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()
    email = models.EmailField()
    phone_number = models.IntegerField()
    address = models.CharField(max_length=255)
    class Meta:
        managed = True

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.age} {self.email} {self.phone_number} {self.address}"


class Pharmacy(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()
    email = models.EmailField()
    phone_number = models.IntegerField()
    address = models.CharField(max_length=255)
    class Meta:
        managed = True

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.age} {self.email} {self.phone_number} {self.address}"


