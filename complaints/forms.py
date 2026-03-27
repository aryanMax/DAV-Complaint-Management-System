from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
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
        fields = ['title', 'category', 'description']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'E.g., Wi-Fi not working in Hostel B',
                'style': 'box-sizing: border-box;'
            }),
            'category': forms.Select(attrs={
                'style': 'box-sizing: border-box;'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Please provide specific details (location, timing, people involved, etc.)...',
                'rows': 5,
                'style': 'box-sizing: border-box;'
            }),
        }
