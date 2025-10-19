from django.shortcuts import render
from accounts.models import PatientRecord

# Create your views here.

def pharmacy_details(request):
    pharma = PatientRecord.objects.all()
    return render(request, 'pharmacy/pharma_dashboard.html', {'pharma': pharma})