from django import forms
from django.contrib.auth.models import User
from .models import Complaint, Notice, LostAndFoundItem

class StudentSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Choose a secure password', 
        'style': 'width: 100%; padding: 12px; background: #0b1120; border: 1px solid #334155; color: white; border-radius: 6px; margin-bottom: 20px; box-sizing: border-box;'
    }))
    password_confirm = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm your password', 
        'style': 'width: 100%; padding: 12px; background: #0b1120; border: 1px solid #334155; color: white; border-radius: 6px; margin-bottom: 20px; box-sizing: border-box;'
    }))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'style': 'width: 100%; padding: 12px; background: #0b1120; border: 1px solid #334155; color: white; border-radius: 6px; margin-bottom: 5px; box-sizing: border-box;'}),
            'email': forms.EmailInput(attrs={'style': 'width: 100%; padding: 12px; background: #0b1120; border: 1px solid #334155; color: white; border-radius: 6px; margin-bottom: 20px; box-sizing: border-box;'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'category', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Brief title of the issue', 'style': 'box-sizing: border-box;'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Provide full details here...', 'style': 'box-sizing: border-box;'}),
        }

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'E.g., Hostel Wi-Fi Maintenance Update', 'style': 'box-sizing: border-box;'}),
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write the full announcement here...', 'style': 'box-sizing: border-box;'}),
        }

# === NEW: LOST & FOUND FORM ===
class LostAndFoundForm(forms.ModelForm):
    class Meta:
        model = LostAndFoundItem
        fields = ['title', 'item_type', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'E.g., Blue Casio Watch', 'style': 'box-sizing: border-box;'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Where was it lost/found? Distinguishing marks?', 'style': 'box-sizing: border-box;'}),
        }
