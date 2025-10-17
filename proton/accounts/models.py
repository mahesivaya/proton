from atexit import register
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
    patient_id = models.CharField(
        max_length=12,
        primary_key=True,
        editable=False,
        unique=True
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()
    email = models.EmailField()
    phone_number = models.IntegerField()
    address = models.CharField(max_length=255)
    visit_reason = models.CharField(max_length=255, default='General Consultation')
    registered_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.patient_id:
            # e.g., PAT12345678
            import random
            self.patient_id = f'PAT{random.randint(10000000, 99999999)}'
        super().save(*args, **kwargs)

    class Meta:
        managed = True

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.age} {self.email} {self.phone_number} {self.address} {self.visit_reason} {self.registered_at} {self.visit_reason}"


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


class PatientRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medical_history = models.TextField()
    allergies = models.TextField()
    medications = models.TextField()

    def __str__(self):
        return f'Record for {self.patient.patient_id}'
