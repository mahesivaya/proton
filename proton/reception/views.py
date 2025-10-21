from audioop import add
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from accounts.decorators import role_required
from accounts.models import Patient, PatientRecord, ScheduleAppointment, PatientMedicine
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.


@role_required(allowed_roles=['reception'])
@login_required
@csrf_exempt
def reception_dashboard(request):
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        age = request.POST.get("age")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        visit_reason = request.POST.get("visit_reason")
        patient = Patient.objects.create(
            first_name=first_name,
            last_name=last_name,
            age=age,
            email=email,
            phone_number=phone_number,
            address=address,
            visit_reason=visit_reason)
        messages.success(request, "Patient registered successfully")
        patient.save()
        return redirect('reception_dashboard')
    # For all Patients 
    patients = Patient.objects.all().order_by('-registered_at')
    all_appointments = ScheduleAppointment.objects.all().order_by('-appointment_date')
    # For Patients registered in the last 1 hour
    one_hour_ago = timezone.now() - timedelta(hours=1)
    recent_patients = Patient.objects.filter(registered_at__gte=one_hour_ago).order_by('-registered_at')
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

    return render(request, 'reception/reception_dashboard.html', {'patients': patients, 'recent_patients': recent_patients, 'searchpatients': searchpatients, 'all_appointments': all_appointments})


@role_required(allowed_roles=['reception', 'doctor'])
@login_required
def patient_details(request, patient_id):
    try:
        patient = Patient.objects.get(patient_id=patient_id)
        patient_records = PatientRecord.objects.get(patient_id = patient_id)
        patient_medicine = PatientMedicine.objects.filter(patient_id=patient_id).order_by('-created_at')
    except Patient.DoesNotExist:
        messages.error(request, "Patient not found")
        return redirect('reception_dashboard')

    return render(request, 'reception/patient_details.html', {'patient': patient, 'patient_records': patient_records, 'patient_medicine':patient_medicine})


@login_required
@role_required(allowed_roles=['reception', 'doctor'])
def patient_records(request, patient_id):
    patient_records = PatientRecord.objects.get(patient_id = patient_id)
    patient_medicine = patient_medicine(patient_id = patient_id)
    return render(request, 'reception/patient_details.html', {'patient_records': patient_records,'patient_medicine':patient_medicine})

# --------------------------------------------
@role_required(allowed_roles=['reception'])
@login_required
@csrf_exempt
def schedule_appointment(request, patient_id):
    patient = Patient.objects.get(patient_id=patient_id)
    reason = Patient.objects.get(patient_id=patient_id).visit_reason
    appointment_date = timezone.now()

    ScheduleAppointment.objects.create(
        patient=patient,
        appointment_date=appointment_date,
        reason=reason
    )
    return redirect('reception_dashboard')


@role_required(allowed_roles=['reception'])
@login_required
def appointments(request):
    all_appointments = ScheduleAppointment.objects.all().order_by('-appointment_date')
    return render(request, 'reception/reception_dashboard.html', {'all_appointments': all_appointments})