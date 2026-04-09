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
    path('priority/', views.priority_complaints_view, name='priority_complaints'), # NEW PRIORITY ROUTE
    path('update/<int:complaint_id>/', views.update_status, name='update_status'),
    path('view/<int:complaint_id>/', views.complaint_detail, name='complaint_detail'),
    
    # --- Authentication Routing ---
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    # --- Notice Board & Lost/Found ---
    path('notice-board/', views.notice_board_view, name='notice_board'),
    path('publish-notice/', views.publish_notice_view, name='publish_notice'),
    path('lost-and-found/', views.lost_and_found_view, name='lost_and_found'),
    path('report-item/', views.report_item_view, name='report_item'),
]
