from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from accounts.decorators import role_required
from django.contrib import messages
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from accounts.models import Patient, PatientRecord, ScheduleAppointment, PatientMedicine

# Create your views here.

@role_required(allowed_roles=['doctor'])
@login_required
def doctor_dashboard(request):
    # all_patients = Patient.objects.all().order_by('-registered_at')
    # today = timezone.now().date()

    now = timezone.now()
    next_hour = now - timedelta(hours=1)
    two_days_ago = now - timedelta(days=2)

    today = timezone.now().date()

    # all_appointments = ScheduleAppointment.objects.select_related('patient').filter(appointment_date__date=today).order_by('-appointment_date')
    all_appointments = ScheduleAppointment.objects.select_related('patient').filter(appointment_date__range=(two_days_ago, now)).order_by('-appointment_date')
    context = {
        # 'all_patients': all_patients,
        'all_appointments': all_appointments,
    }   
    return render(request, 'doctor/doctor_dashboard.html', context)


@login_required
@role_required(allowed_roles=['doctor'])
def patient_records(request, patient_id):
    patient_records = PatientRecord.objects.get(patient_id = patient_id)
    return render(request, 'doctor/patient_details.html', {'patient_records': patient_records})


@role_required(allowed_roles=['doctor'])
def patient_medicine(request, patient_id):
    patient = Patient.objects.get(patient_id=patient_id)
    if request.method == "POST":
        form_data = request.POST.dict()
        form_data.pop('csrfmiddlewaretoken', None)
        # patient = get_object_or_404(Patient, id=patient_id)
        PatientMedicine.objects.create(
            patient=patient,
            medicine=form_data)
        messages.success(request, "Patient registered successfully")
        return render(request, 'patient_dashboard.html', patient_id=patient_id)
    return render(request, 'reception/reception_dashboard.html')


@role_required(allowed_roles=['doctor'])
def patient_dashboard(request, patient_id):
    patient = Patient.objects.get(patient_id=patient_id)
    patient_medicine = PatientMedicine.objects.filter(patient_id=patient_id)
    return render(request, 'doctor/patient_dashboard.html', {'patient_medicine': patient_medicine, 'patient': patient})

# @role_required(allowed_roles=['reception', 'doctor'])
# @login_required
# def patient_details(request, patient_id):
#     try:
#         patient = Patient.objects.get(patient_id=patient_id)
#         # patient_records = PatientRecord.objects.get(patient_id = patient_id)
#         patient_medicine = PatientMedicine.objects.filter(patient_id=patient_id).order_by('-created_at')
#     except Patient.DoesNotExist:
#         messages.error(request, "Patient not found")
#         return redirect('reception_dashboard')

#     return render(request, 'reception/patient_details.html', {'patient': patient, 'patient_medicine':patient_medicine})
