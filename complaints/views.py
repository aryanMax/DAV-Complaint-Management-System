from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils import timezone
from datetime import timedelta

from .models import Complaint, Notice, LostAndFoundItem
from .forms import ComplaintForm, StudentSignUpForm, NoticeForm, LostAndFoundForm

def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    recent_notices = Notice.objects.all().order_by('-created_at')[:5]
    return render(request, 'complaints/home.html', {'notices': recent_notices})

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
            login(request, user)
            return redirect('dashboard')
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

# === UPDATED PRIORITY VIEW (ADMIN ONLY) ===
@login_required
def priority_complaints_view(request):
    # Security Check: Only allow Admins
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to view priority complaints.")

    # Calculate exactly 3 days ago from this exact moment
    three_days_ago = timezone.now() - timedelta(days=3)

    # Admins see all unresolved complaints older than 3 days
    complaints = Complaint.objects.filter(
        status__in=['PENDING', 'IN_PROGRESS'],
        created_at__lte=three_days_ago
    ).order_by('created_at') # ordered ascending (oldest first)

    return render(request, 'complaints/priority_complaints.html', {'complaints': complaints})

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
        
    if request.method == 'POST' and request.user == complaint.created_by and complaint.status == 'RESOLVED' and not complaint.rating:
        rating = request.POST.get('rating')
        feedback_text = request.POST.get('feedback_text')
        
        if rating:
            complaint.rating = int(rating)
            complaint.feedback_text = feedback_text
            complaint.save()
            messages.success(request, "Thank you for rating the resolution!")
            return redirect('complaint_detail', complaint_id=complaint.id)
        else:
            messages.error(request, "Please select a star rating.")

    return render(request, 'complaints/complaint_detail.html', {'complaint': complaint})

@login_required
def notice_board_view(request):
    notices = Notice.objects.all().order_by('-created_at')
    return render(request, 'complaints/notice_board.html', {'notices': notices})

@login_required
def publish_notice_view(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to publish notices.")
    
    if request.method == 'POST':
        form = NoticeForm(request.POST)
@login_required
def notice_board_view(request):
    notices = Notice.objects.all().order_by('-created_at')
    return render(request, 'complaints/notice_board.html', {'notices': notices})

@login_required
def publish_notice_view(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to publish notices.")
    
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.created_by = request.user
            notice.save()
            messages.success(request, "Notice published successfully!")
            return redirect('notice_board')
    else:
        form = NoticeForm()
    return render(request, 'complaints/publish_notice.html', {'form': form})

@login_required
def lost_and_found_view(request):
    items = LostAndFoundItem.objects.filter(is_resolved=False).order_by('-created_at')
    return render(request, 'complaints/lost_and_found.html', {'items': items})

@login_required
def report_item_view(request):
    if request.method == 'POST':
        form = LostAndFoundForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            messages.success(request, "Item reported successfully!")
            return redirect('lost_and_found')
    else:
        form = LostAndFoundForm()
    return render(request, 'complaints/report_item.html', {'form': form})
