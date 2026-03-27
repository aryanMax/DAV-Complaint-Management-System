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
        class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        # Added 'category' to the fields list!
        fields = ['title', 'category', 'description']
        
        # Adding placeholders and making sure inputs stay inside their boxes
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
