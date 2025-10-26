from audioop import add
import re
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from accounts.decorators import role_required
from accounts.models import Patient, ScheduleAppointment, PatientMedicine
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.


@role_required(allowed_roles=['reception', 'admin', 'doctor'])
@login_required
@csrf_exempt
def reception_dashboard(request):
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        visit_reason = request.POST.get("visit_reason")
        referral = request.POST.get("referral")
        fee = request.POST.get("fee")
        patient = Patient.objects.create(
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            email=email,
            phone_number=phone_number,
            address=address,
            visit_reason=visit_reason,
            referral=referral,
            fee=fee)
        messages.success(request, "Patient registered successfully")
        patient.save()
        return redirect('reception_dashboard')
    # For all Patients 
    patients = Patient.objects.all().order_by('-registered_at')
    #all_appointments = ScheduleAppointment.objects.all().order_by('-appointment_date')
    # For Patients registered in the last 1 hour
    one_day_ago = timezone.now() - timedelta(hours=24)
    all_appointments = ScheduleAppointment.objects.filter(appointment_date__gte=one_day_ago).order_by('-appointment_date')
    recent_patients = Patient.objects.filter(registered_at__gte=one_day_ago).order_by('-registered_at')
    have_appointments = ScheduleAppointment.objects.values_list('patient_id', flat=True)
    query = request.GET.get('q')
    if query:
        searchpatients = Patient.objects.filter(
            Q(patient_id__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(address__icontains=query)
        )
    else:
        searchpatients = Patient.objects.none()

    return render(request, 'reception/reception_dashboard.html', {'patients': patients, 'recent_patients': recent_patients, 'searchpatients': searchpatients, 'all_appointments': all_appointments, 'have_appointments': list(have_appointments)})


@role_required(allowed_roles=['reception', 'doctor'])
@login_required
def patient_details(request, patient_id):
    try:
        patient = Patient.objects.get(patient_id=patient_id)
        #patient_records = PatientRecord.objects.get(patient_id = patient_id)
        patient_medicine = PatientMedicine.objects.filter(patient_id=patient_id).order_by('-created_at')
    except Patient.DoesNotExist:
        messages.error(request, "Patient not found")
        return redirect('reception_dashboard')

    return render(request, 'reception/patient_details.html', {'patient': patient, 'patient_medicine':patient_medicine})


@login_required
@role_required(allowed_roles=['reception', 'doctor'])
def patient_records(request, patient_id):
    #patient_records = PatientRecord.objects.get(patient_id = patient_id)
    patient_medicine = patient_medicine(patient_id = patient_id)
    return render(request, 'reception/patient_details.html', {'patient_medicine':patient_medicine})

# --------------------------------------------
@role_required(allowed_roles=['reception'])
@login_required
@csrf_exempt
def schedule_appointment(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)

    # Optional: get the reason from patient object
    reason = patient.visit_reason if hasattr(patient, 'visit_reason') else ''

    # Prevent duplicate appointment for the same day
    today = timezone.now().date()
    exists = ScheduleAppointment.objects.filter(
        patient=patient,
        appointment_date__date=today
    ).exists()

    if exists:
        messages.warning(request, "This patient already has an appointment today.")
        return redirect('reception_dashboard')

    # Create the appointment
    ScheduleAppointment.objects.create(
        patient=patient,
        appointment_date=timezone.now(),
        reason=reason
    )

    messages.success(request, "Appointment scheduled successfully.")
    return redirect('reception_dashboard')



@role_required(allowed_roles=['reception'])
@login_required
def appointments(request):
    all_appointments = ScheduleAppointment.objects.all().order_by('-appointment_date')
    return render(request, 'reception/reception_dashboard.html', {'all_appointments': all_appointments})
