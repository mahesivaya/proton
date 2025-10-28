from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from accounts.models import Pharmacy, Patient, PatientMedicine
from collections import defaultdict
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from collections import defaultdict
from django.utils import timezone
from django.shortcuts import render

from doctors.views import patient_medicine
# Create your views here.
from collections import defaultdict
from django.utils import timezone
from django.shortcuts import render
from accounts.models import Patient, PatientMedicine

from collections import defaultdict
from django.utils import timezone
from django.shortcuts import render
from itertools import groupby


@role_required(allowed_roles=['pharmacy', 'admin'])
@login_required

def pharmacy_dashboard(request):
    # Current local date
    today = timezone.localdate()

    # Fetch patients registered today
    todays_patients = Patient.objects.filter(
        registered_at__date=today
    ).order_by('-registered_at')

    # Fetch medicines prescribed today for these patients
    todays_medicines = PatientMedicine.objects.filter(
        patient__in=todays_patients,
        created_at__date=today
    ).order_by('patient', '-created_at')

    # Prepare a list of patients with their visits
    patients_with_visits = []

    for patient in todays_patients:
        # Get medicines for this patient
        meds = [med for med in todays_medicines if med.patient == patient]

        # Group medicines by visit (prescriptions within 5 minutes)
        visits = []
        if meds:
            current_visit_time = meds[0].created_at
            current_visit_meds = []

            for med in meds:
                if (current_visit_time - med.created_at).total_seconds() > 300:  # >5min → new visit
                    visits.append({
                        "visit_time": current_visit_time,
                        "medicines": current_visit_meds
                    })
                    current_visit_meds = []
                    current_visit_time = med.created_at
                current_visit_meds.append(med)

            if current_visit_meds:
                visits.append({
                    "visit_time": current_visit_time,
                    "medicines": current_visit_meds
                })

        patients_with_visits.append({
            "patient": patient,
            "visits": visits
        })

    return render(request, "pharmacy/pharmacy_dashboard.html", {
        "patients_with_visits": patients_with_visits
    })