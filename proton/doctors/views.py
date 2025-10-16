from django.shortcuts import render

from accounts.decorators import role_required
from django.contrib.auth.decorators import login_required
from accounts.models import Patient

# Create your views here.

@role_required(allowed_roles=['doctor'])
@login_required
def doctor_dashboard(request):
    all_patients = Patient.objects.all().order_by('-registered_at')
    return render(request, 'doctor/doctor_dashboard.html', {'all_patients': all_patients})