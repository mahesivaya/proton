import datetime
import email
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import role_required
from accounts.models import Patient, ScheduleAppointment
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


ROLE_REDIRECTS = {
    'admin': 'admin_dashboard',
    'reception': 'reception_dashboard',
    'doctor': 'doctor_dashboard',
    'nurse': 'nurse_dashboard',
    'patient': 'patient_dashboard',
    'pharmacy': 'pharmacy_dashboard',
}

def redirect_to_role_home(user):
    """Redirect user to their role-specific home/dashboard."""
    redirect_url = ROLE_REDIRECTS.get(user.role)
    if redirect_url:
        return redirect(redirect_url)
    else:
        return redirect('home')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect based on role
            return redirect_to_role_home(user)
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'accounts/login.html')

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    messages.info(request, "You have logged out.")
    return redirect('home')


@role_required(allowed_roles=['admin'])
@login_required
def admin_dashboard(request):
    return render(request, 'executive/executive.html')

def unauthorized_view(request):
    return render(request, 'unauthorized.html', status=403)

@role_required(allowed_roles=['admin', 'reception', 'doctor', 'nurse', 'patient', 'pharmacy'])
@login_required
def redirect_to_home(request):
    """Redirect logged-in users to their dashboard based on role."""
    user = request.user
    return redirect_to_role_home(user)



from django.shortcuts import render

def about(request):
    return render(request, "accounts/about.html")

def treatment(request):
    return render(request, "accounts/treatment.html")

def contact(request):
    return render(request, "accounts/contact.html")

def home(request):
    return render(request, "accounts/home.html")

def appointment(request):
    if request.method == 'POST':
        # Handle form submission
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        visit_reason = request.POST.get('visit_reason')
        referral = request.POST.get('referral')
        registered_at = request.POST.get('registered_at')
        print("📞 Phone received:", phone_number)

        if not phone_number:
            messages.error(request, "Phone number is required.")

        patient = Patient.objects.create(
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            email=email,
            phone_number=phone_number,
            visit_reason=visit_reason,
            referral=referral,
        )
        patient.save()
        appointment = ScheduleAppointment.objects.create(
            patient=patient,
            appointment_date=registered_at,
            reason=visit_reason
        )
        appointment.save()
        return redirect('home')

    return render(request, "accounts/appointment.html")



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication



class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


from rest_framework_simplejwt.views import TokenObtainPairView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class CsrfExemptObtainTokenPairView(TokenObtainPairView):
    pass


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login

User = get_user_model()

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        # Hard-coded default role
        role = "patient"

        # Validation
        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        # Create user with default patient role
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            phone_number=phone,
            address=address
        )

        messages.success(request, "Registration successful. Please log in.")
        return redirect("login")

    return render(request, "accounts/register.html")
