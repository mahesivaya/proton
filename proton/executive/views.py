from django.shortcuts import render
from django.db.models.functions import ExtractMonth
import calendar
from django.shortcuts import redirect
from django.http import request
from django.shortcuts import render
from accounts.models import ScheduleAppointment
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.shortcuts import render
from accounts.models import Patient
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from django.utils import timezone
from datetime import datetime, date, time
import calendar
from django.db.models.functions import ExtractYear, ExtractMonth
from collections import defaultdict
import calendar, json




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
        .order_by('-registration_date')
    )
    dates = (
        Patient.objects
        .annotate(year=ExtractYear('registered_at'), month=ExtractMonth('registered_at'))
        .values('year', 'month')
        .distinct()
        .order_by('year', 'month')
    )
    years_months = defaultdict(list)
    for r in dates:
        month_name = calendar.month_name[r['month']]
        years_months[r['year']].append({'month': r['month'], 'month_name': month_name})


    monthly_data = (
        Patient.objects
        .annotate(year=ExtractYear('registered_at'), month=ExtractMonth('registered_at'))
        .values('year', 'month')
        .annotate(total=Count('patient_id'))
        .order_by('year', 'month')
    )

    # Add month names (e.g. 1 → January)
    for entry in monthly_data:
        entry['month_name'] = calendar.month_name[entry['month']]

    context = {
        'patients': patients,
        'todays_scheduled_appointments': list(todays_scheduled_appointments),
        'patients_per_day': patients_per_day,
        'dates': dates,
        'years_months': dict(years_months),
        'monthly_data': monthly_data
    }

    return render(request, 'executive/executive.html', context)


@role_required(allowed_roles=['admin'])
@login_required
def monthly_patients(request, year, month):
    """Displays patients registered in the selected year and month"""
    try:
        start_date = timezone.make_aware(datetime(year, month, 1))
        end_date = timezone.make_aware(datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59))

        patients = Patient.objects.filter(registered_at__range=(start_date, end_date)).order_by('-registered_at')
    except Exception:
        patients = Patient.objects.none()

    monthly_data = (
        Patient.objects
        .annotate(year=ExtractYear('registered_at'), month=ExtractMonth('registered_at'))
        .values('year', 'month')
        .annotate(total=Count('patient_id'))
        .order_by('year', 'month')
    )

    # Prepare labels and values for the chart
    labels = []
    values = []
    for row in monthly_data:
        label = f"{calendar.month_name[row['month']]} {row['year']}"
        labels.append(label)
        values.append(row['total'])

    context = {
        'patients': patients,
        'year': year,
        'month': month,
        'labels': json.dumps(labels),
        'values': json.dumps(values),

    }
    return render(request, 'executive/monthly_patients.html', context)


@role_required(allowed_roles=['admin'])
@login_required
def patient_filter_form(request):
    """Shows the form and optionally displays filtered patients"""
    if request.method == 'POST':
        year = request.POST.get('year')
        month = request.POST.get('month')
        return redirect('monthly_patients', year=year, month=month)
    
    # Just render the form initially
    return render(request, 'executive/monthly_patients.html')


@role_required(allowed_roles=['admin'])
@login_required
def yearly_patients(request, year):
    """Displays patients registered in the selected year"""
    try:
        start_date = timezone.make_aware(datetime(year, 1, 1))
        end_date = timezone.make_aware(datetime(year, 12, 31, 23, 59, 59))

        patients = Patient.objects.filter(registered_at__range=(start_date, end_date)).order_by('-registered_at')
    except Exception:
        patients = Patient.objects.none()

    months = (
        Patient.objects.filter(registered_at__year=year)
        .annotate(month=ExtractMonth('registered_at'))
        .values_list('month', flat=True)
        .distinct()
        .order_by('month')
    )

    # Create (month_number, month_name) tuples
    month_data = [(m, calendar.month_name[m]) for m in months]
    context = {
        'patients': patients,
        'year': year,
        'month_data':month_data
    }
    return render(request, 'executive/yearly_patients.html', context)

