from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import role_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import Patient, PatientRecord, ScheduleAppointment, PatientMedicine

# Create your views here.

@role_required(allowed_roles=['doctor'])
@login_required
def doctor_dashboard(request):
    # all_patients = Patient.objects.all().order_by('-registered_at')
    all_appointments = ScheduleAppointment.objects.select_related('patient').all()
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
        return redirect('dashboard')
    return render(request, 'reception/reception_dashboard.html')    