from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

# Import your models and forms
from .models import Complaint
from .forms import ComplaintForm, StudentSignUpForm

# ==========================================
# AUTHENTICATION VIEWS
# ==========================================

def signup_view(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard') 
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
            # Check if the selected role matches their actual staff status
            if login_type == 'admin' and user.is_staff:
                login(request, user)
                return redirect('dashboard')
            elif login_type == 'student' and not user.is_staff:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid role for this account.")
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


# ==========================================
# DASHBOARD & COMPLAINT VIEWS
# ==========================================

@login_required
def dashboard_view(request):
    # Route admins and students to their respective templates
    # and fetch the correct complaints for the stats counters
    if request.user.is_staff:
        complaints = Complaint.objects.all()
        template_name = 'admin_dashboard.html'
    else:
        complaints = Complaint.objects.filter(created_by=request.user)
        template_name = 'student_dashboard.html'

    context = {
        'total': complaints.count(),
        'pending': complaints.filter(status='PENDING').count(),
        'resolved': complaints.filter(status='RESOLVED').count(),
    }
    return render(request, template_name, context)

@login_required
def create_complaint_view(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.created_by = request.user
            complaint.save()
            return redirect('dashboard')
    else:
        form = ComplaintForm()
    return render(request, 'complaints/create_complaint.html', {'form': form})

@login_required
def my_complaints_view(request):
    complaints = Complaint.objects.filter(created_by=request.user)
    return render(request, 'complaints/my_complaints.html', {'complaints': complaints})

@login_required
def all_complaints_view(request):
    # Security check: Only admins can view all complaints
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to view this page.")
        
    complaints = Complaint.objects.all()
    return render(request, 'complaints/all_complaints.html', {'complaints': complaints})

@login_required
def update_status(request, complaint_id):
    # Security check: Only admins can update statuses
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to update complaints.")
        
    complaint = get_object_or_404(Complaint, id=complaint_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        complaint.status = new_status
        complaint.save()
        return redirect('all_complaints')

    return render(request, 'complaints/update_status.html', {'complaint': complaint})
