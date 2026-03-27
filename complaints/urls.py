from django.urls import path
from . import views

urlpatterns = [
    # --- Authentication Routing ---
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    # --- Dashboard & Complaint Routing ---
    path('', views.dashboard_view, name='dashboard'), 
    path('create/', views.create_complaint_view, name='create_complaint'),
    path('my/', views.my_complaints_view, name='my_complaints'),
    path('all/', views.all_complaints_view, name='all_complaints'),
    
    # This URL passes the specific complaint ID to the view
    path('update/<int:complaint_id>/', views.update_status, name='update_status'),
]
