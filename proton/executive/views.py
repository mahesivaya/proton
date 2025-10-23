from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from accounts.models import ScheduleAppointment
# Create your views here.
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.shortcuts import render
from accounts.models import Patient
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required



@role_required(allowed_roles=['admin'])
@login_required
def admin_dashboard(request):
    # All patients
    patients = Patient.objects.all().order_by('-registered_at')
    
    # Patients scheduled today (same as before)
    from django.utils import timezone
    today = timezone.now().date()
    todays_scheduled_appointments = ScheduleAppointment.objects.filter(
        appointment_date__date=today
    ).values_list('patient__patient_id', flat=True)

    # Total patients per day
    patients_per_day = (
        Patient.objects
        .annotate(registration_date=TruncDate('registered_at'))
        .values('registration_date')
        .annotate(total_patients=Count('patient_id'))
        .order_by('registration_date')
    )

    context = {
        'patients': patients,
        'todays_scheduled_appointments': list(todays_scheduled_appointments),
        'patients_per_day': patients_per_day
    }

    return render(request, 'executive/executive.html', context)
