from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # This forwards all other traffic to the complaints app's urls.py
    path('', include('complaints.urls')), 
]
