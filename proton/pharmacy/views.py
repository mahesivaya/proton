from django.shortcuts import render
from accounts.models import PatientRecord
from proton.accounts.decorators import role_required

# Create your views here.

def pharmacy_details(request):
    pharma = PatientRecord.objects.all()
    return render(request, 'pharmacy/pharma_dashboard.html', {'pharma': pharma})


from django.shortcuts import render, redirect
import json

    
