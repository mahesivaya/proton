from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import role_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import Patient, PatientRecord, ScheduleAppointment, PatientMedicine
from datetime import timedelta
from django.utils import timezone
# Create your views here.

@role_required(allowed_roles=['doctor'])
@login_required
def doctor_dashboard(request):
    # all_patients = Patient.objects.all().order_by('-registered_at')
    # all_appointments = ScheduleAppointment.objects.select_related('patient').all()
    one_day_ago = timezone.now() - timedelta(hours=24)
    all_appointments = ScheduleAppointment.objects.filter(appointment_date__gte=one_day_ago).order_by('-appointment_date')
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
        return redirect('patient_details', patient_id=patient_id)
    return render(request, 'reception/reception_dashboard.html')    
