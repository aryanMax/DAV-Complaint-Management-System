from django.urls import path
from . import views

urlpatterns = [
   # --- Dashboard & Complaint Routing ---
    path('', views.home_view, name='home'), # New Landing Page
    path('dashboard/', views.dashboard_view, name='dashboard'), # Moved Dashboard
    path('create/', views.create_complaint_view, name='create_complaint'),
    path('my/', views.my_complaints_view, name='my_complaints'),
    path('all/', views.all_complaints_view, name='all_complaints'),
    path('update/<int:complaint_id>/', views.update_status, name='update_status'),
]
