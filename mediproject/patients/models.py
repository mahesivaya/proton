# Create your models here.
from django.db import models

# Create your models here.
class Patient(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='patients/images/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email} {self.phone_number} {self.address} {self.city} {self.state} {self.zip_code} {self.country} {self.profile_picture}"

class PatientImage(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='patients/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} - {self.image.name}"
class Pharmacy(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='pharmacies')
    medicine_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    prescribed_on = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.medicine_name} for {self.patient.first_name} {self.patient.last_name}"