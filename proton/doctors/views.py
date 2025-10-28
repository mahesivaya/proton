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


from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from accounts.models import Patient, PatientMedicine

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
@role_required(allowed_roles=['doctor', 'pharmacy'])
@login_required
def patient_medicine(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)

    if request.method == "POST":
        # Extract form data
        name = request.POST.get("medicinename")
        dose = request.POST.get("medicinedose")
        duration = request.POST.get("medicineduration")
        notes = request.POST.get("notes")

        # Handle frequency (days)
        frequency = request.POST.get("frequency")
        custom_frequency = request.POST.get("custom_frequency")
        final_frequency = custom_frequency if frequency == "other" and custom_frequency else f"Every {frequency} Day(s)"

        # Handle time periods (multi-select)
        time_periods = request.POST.getlist("time_period")
        custom_time_period = request.POST.get("custom_time_period")
        if "other" in time_periods and custom_time_period:
            time_periods.remove("other")
            time_periods.append(custom_time_period)
        final_time_period = ", ".join(tp.capitalize() for tp in time_periods)

        # Save medicine for patient
        PatientMedicine.objects.create(
            patient=patient,
            medicine={
                "name": name,
                "dose": dose,
                "frequency": final_frequency,
                "time_period": final_time_period,
                "duration": duration,
                "notes": notes
            }
        )

        messages.success(request, f"Medicine '{name}' added for {patient.first_name}.")
        return redirect("patient_details", patient_id=patient_id)

    return render(request, "executive/patient_medicine.html", {"patient": patient})