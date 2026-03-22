from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = False # Ensures they are a student, not an admin
        if commit:
            user.save()
        return user