from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import role_required


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
        return redirect('login')

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
    return redirect('login')


@role_required(allowed_roles=['admin'])
@login_required
def admin_dashboard(request):
    return render(request, 'accounts/admin_dashboard.html')

def unauthorized_view(request):
    return render(request, 'unauthorized.html', status=403)

@role_required(allowed_roles=['admin', 'reception', 'doctor', 'nurse', 'patient', 'pharmacy'])
@login_required
def redirect_to_home(request):
    """Redirect logged-in users to their dashboard based on role."""
    user = request.user
    return redirect_to_role_home(user)
