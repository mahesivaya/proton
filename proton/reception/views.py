from audioop import add
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from accounts.decorators import role_required
from accounts.models import Patient
from django.contrib import messages

# Create your views here.


@role_required(allowed_roles=['reception'])
@login_required
def reception_dashboard(request):
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        age = request.POST.get("age")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        patient = Patient.objects.create(first_name=first_name,last_name=last_name, age=age, email=email,phone_number=phone_number,address=address)
        messages.success(request, "Patient registered successfully")
        patient.save()
        return redirect('reception_dashboard')
    all_patients = Patient.objects.all().order_by('-registered_at')
    return render(request, 'reception/reception_dashboard.html', {'all_patients': all_patients})


@role_required(allowed_roles=['reception'])
@login_required
def patient_details(request, patient_id):
    try:
        patient = Patient.objects.get(id=patient_id)
    except Patient.DoesNotExist:
        messages.error(request, "Patient not found")
        return redirect('reception_dashboard')

    return render(request, 'reception/patient_details.html', {'patient': patient})