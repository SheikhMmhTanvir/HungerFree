# core/views.py

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import User, Donation, Delivery
from .forms import SignUpForm, LoginForm

# 1. Landing Page View
class LandingPageView(TemplateView):
    template_name = "landing_page.html"

# 2. Sign-Up View
def signup_view(request):
    role = request.GET.get('role', 'donor').upper()
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = role  # Set the role from the modal
            user.save()
            login(request, user) # Log the user in
            return redirect('dashboard')
    else:
        form = SignUpForm()

    context = {
        'role': role.capitalize(),
        'form': form
    }
    return render(request, "auth/signup.html", context)

# 3. Login View
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, "auth/login.html", {'form': form})

# 4. Logout View
def logout_view(request):
    logout(request)
    return redirect('landing_page')

# 5. Main Dashboard View (Role-based)
@login_required
def dashboard_view(request):
    user = request.user

    if user.role == User.Role.DONOR:
        donations = Donation.objects.filter(donor=user).order_by('-created_at')
        context = {'donations': donations}
        return render(request, "dashboard/donor.html", context)
    
    elif user.role == User.Role.RECEIVER:
        available_donations = Donation.objects.filter(status=Donation.DonationStatus.PENDING)
        context = {'available_donations': available_donations}
        return render(request, "dashboard/receiver.html", context)
        
    elif user.role == User.Role.VOLUNTEER:
        pending_deliveries = Delivery.objects.filter(status=Delivery.DeliveryStatus.PENDING)
        context = {'pending_deliveries': pending_deliveries}
        return render(request, "dashboard/volunteer.html", context)
    
    return redirect('landing_page')