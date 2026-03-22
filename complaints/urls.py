from django.urls import path
from . import views

urlpatterns = [
    # Main dashboard and complaint routing
    path('', views.dashboard_view, name='dashboard'), 
    path('create/', views.create_complaint_view, name='create_complaint'),
    path('my/', views.my_complaints_view, name='my_complaints'),
    path('all/', views.all_complaints_view, name='all_complaints'),
    
    # Authentication routing
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]