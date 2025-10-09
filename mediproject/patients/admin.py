from django.contrib import admin

# Register your models here.
from .models import Patient, PatientImage

class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'city', 'state', 'country', 'uploaded_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    list_filter = ('city', 'state', 'country', 'uploaded_at')