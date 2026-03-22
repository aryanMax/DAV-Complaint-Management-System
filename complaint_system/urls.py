from django.contrib import admin
from django.urls import path
from complaints import views  # Fixed: Imported directly from the app, not from urls

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- Authentication URLs ---
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'), 
    
    # --- Dashboard and Complaint URLs ---
    path('', views.dashboard_view, name='dashboard'),
    path('create/', views.create_complaint_view, name='create_complaint'),
    path('my/', views.my_complaints_view, name='my_complaints'),
    path('all/', views.all_complaints_view, name='all_complaints'),
]