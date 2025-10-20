from django.shortcuts import render

from accounts.decorators import role_required
from django.contrib.auth.decorators import login_required
from accounts.models import Patient, PatientRecord, ScheduleAppointment

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
