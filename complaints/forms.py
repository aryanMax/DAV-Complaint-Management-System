from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Make sure you have a Complaint model in your models.py!
from .models import Complaint 

class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = False 
        if commit:
            user.save()
        return user

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        # Note: Change these to match your actual database fields!
        fields = ['title', 'description']