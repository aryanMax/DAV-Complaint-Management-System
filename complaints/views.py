# Update this line at the top of views.py
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Complaint
from .forms import ComplaintForm
from django.http import HttpResponseForbidden
from django.shortcuts import render



@login_required
def dashboard(request):
    complaints = Complaint.objects.filter(created_by=request.user)

    context = {
        'total': complaints.count(),
        'pending': complaints.filter(status='PENDING').count(),
        'resolved': complaints.filter(status='RESOLVED').count(),
    }

    return render(request, 'complaints/dashboard.html', context)




@login_required
def create_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.created_by = request.user
            complaint.save()
            return redirect('/')

    else:
        form = ComplaintForm()

    return render(request, 'complaints/create_complaint.html', {'form': form})


@login_required
def my_complaints(request):
    complaints = Complaint.objects.filter(created_by=request.user)
    return render(request, 'complaints/my_complaints.html', {'complaints': complaints})


@login_required
def all_complaints(request):
    if request.user.profile.role != 'ADMIN':
        return HttpResponseForbidden("You are not authorized to view this page.")

    complaints = Complaint.objects.all()
    return render(request, 'complaints/all_complaints.html', {'complaints': complaints})


@login_required
def update_status(request, complaint_id):
    if request.user.profile.role != 'ADMIN':
        return HttpResponseForbidden("You are not authorized to update complaints.")

    complaint = Complaint.objects.get(id=complaint_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        complaint.status = new_status
        complaint.save()
        return redirect('all_complaints')

    return render(request, 'complaints/update_status.html', {'complaint': complaint})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# If you created the StudentSignUpForm in forms.py, import it:
# from .forms import StudentSignUpForm 

# --- Add these two functions to the bottom of complaints/views.py ---

def signup_view(request):
    # Note: If you haven't made forms.py yet, you can temporarily use UserCreationForm here
    # form = UserCreationForm(request.POST or None)
    from .forms import StudentSignUpForm 
    
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard') # Make sure this matches your dashboard URL name
    else:
        form = StudentSignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        login_type = request.POST.get('login_type') 
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if login_type == 'admin' and user.is_staff:
                login(request, user)
                return redirect('dashboard') # Admin dashboard URL
            elif login_type == 'student' and not user.is_staff:
                login(request, user)
                return redirect('dashboard') # Student dashboard URL
            else:
                messages.error(request, "Invalid role for this account.")
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'login.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# --- Add these to the bottom of complaints/views.py ---

@login_required
def dashboard_view(request):
    # This checks if the logged-in user is an admin or a student 
    # and sends them to the correct dashboard template
    if request.user.is_staff:
        return render(request, 'admin_dashboard.html')
    else:
        return render(request, 'student_dashboard.html')

@login_required
def create_complaint_view(request):
    return render(request, 'create_complaint.html')

@login_required
def my_complaints_view(request):
    return render(request, 'my_complaints.html')

@login_required
def all_complaints_view(request):
    return render(request, 'all_complaints.html')
def logout_view(request):
    logout(request) # This destroys the user's session safely
    return redirect('login') # Sends them right back to the login screen
