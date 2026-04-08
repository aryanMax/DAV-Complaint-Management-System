from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from .models import Complaint
from .forms import ComplaintForm, StudentSignUpForm

def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'complaints/home.html')

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

@login_required
def dashboard_view(request):
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
        form = ComplaintForm(request.POST, request.FILES)
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
    complaints = Complaint.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'complaints/my_complaints.html', {'complaints': complaints})

@login_required
def all_complaints_view(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to view this page.")
        
    complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, 'complaints/all_complaints.html', {'complaints': complaints})

@login_required
def update_status(request, complaint_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to update complaints.")
        
    complaint = get_object_or_404(Complaint, id=complaint_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        admin_response = request.POST.get('admin_response')
        custom_response = request.POST.get('custom_response')

        complaint.status = new_status
        
        # Save the custom comment or the selected predefined comment
        if admin_response == 'custom':
            complaint.admin_response = custom_response
        elif admin_response:
            complaint.admin_response = admin_response

        complaint.save()
        return redirect('all_complaints')

    return render(request, 'complaints/update_status.html', {'complaint': complaint})

@login_required
def complaint_detail(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    if not request.user.is_staff and complaint.created_by != request.user:
        return HttpResponseForbidden("You are not authorized to view this complaint.")
        
    return render(request, 'complaints/complaint_detail.html', {'complaint': complaint})
