from django.urls import path
from . import views

urlpatterns = [
    # --- Landing & Dashboard Routing ---
    path('', views.home_view, name='home'), 
    path('dashboard/', views.dashboard_view, name='dashboard'), 
    
    # --- Complaint Management Routing ---
    path('create/', views.create_complaint_view, name='create_complaint'),
    path('my/', views.my_complaints_view, name='my_complaints'),
    path('all/', views.all_complaints_view, name='all_complaints'),
    path('update/<int:complaint_id>/', views.update_status, name='update_status'),
    path('view/<int:complaint_id>/', views.complaint_detail, name='complaint_detail'),
    
    # --- Authentication Routing (This is what was missing!) ---
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]
