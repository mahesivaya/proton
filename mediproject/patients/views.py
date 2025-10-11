from tkinter import image_names
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

# Create your views here.
from hmac import new
from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.template import context
from .models import Patient, PatientImage
# from .models import Patient, UploadedFile
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Patient, PatientImage, Pharmacy
from django.shortcuts import render, get_object_or_404
from patients.models import Patient
from django.shortcuts import render, get_object_or_404
from .models import Patient, PatientImage



# Create your views here.from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Patient, PatientImage

def register_patient(request):
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip_code = request.POST.get("zip_code")
        country = request.POST.get("country")
        profile_pictures = request.FILES.getlist("profile_picture")

        # Create patient
        patient = Patient.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            country=country
        )

        # Save each uploaded image
        for image in profile_pictures:
            PatientImage.objects.create(patient=patient, image=image)

        messages.success(request, "Patient registered successfully!")
        return redirect('patient_detail', patient_id=patient.id)

    return render(request, 'patients/register_patient.html')


def upload_images(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        uploaded_images = request.FILES.getlist("profile_picture")

        for image_file in uploaded_images:
            PatientImage.objects.create(patient=patient, image=image_file)

        messages.success(request, "Images uploaded successfully!")

    return redirect('patient_detail', patient_id=patient_id)

def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    images = PatientImage.objects.filter(patient=patient)
    pharmacy = Pharmacy.objects.all()
    return render(request, 'patients/patient_detail.html', {'patient': patient, 'images': images, 'pharmacy': pharmacy})


def all_patients(request):
    patients = Patient.objects.all()
    context = {'patients': patients}
    return render(request, 'patients/all_patients.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Patient, Pharmacy

def add_prescription(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        medicine_name = request.POST.get('medicine_name')
        quantity = request.POST.get('quantity')
        notes = request.POST.get('notes')

        if medicine_name and quantity:
            Pharmacy.objects.create(
                patient=patient,
                medicine_name=medicine_name,
                quantity=int(quantity),
                notes=notes
            )
            messages.success(request, "Prescription added successfully")
        else:
            messages.error(request, "Medicine name and quantity are required")

        return redirect('patient_detail', patient_id=patient.id)

    return render(request, 'patients/patient_prescriptions.html', {'patient': patient})


@login_required
def pharmacy_dashboard(request):
    # pharma = Pharmacy.objects.all()
    pharma = Pharmacy.objects.select_related('patient').all()
    return render(request, 'accounts/pharmacy_dashboard.html', {'pharma': pharma})

