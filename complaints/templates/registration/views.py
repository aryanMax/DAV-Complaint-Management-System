from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import StudentSignUpForm

def signup_view(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('student_dashboard') # Replace with your actual URL name
    else:
        form = StudentSignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        login_type = request.POST.get('login_type') # 'student' or 'admin'
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if login_type == 'admin' and user.is_staff:
                login(request, user)
                return redirect('admin_dashboard') # Replace with your actual URL name
            elif login_type == 'student' and not user.is_staff:
                login(request, user)
                return redirect('student_dashboard')
            else:
                messages.error(request, "Invalid role for this account.")
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'login.html')