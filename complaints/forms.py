class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        # Added 'image' to the fields list!
        fields = ['title', 'category', 'description', 'image']
        
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'E.g., Wi-Fi not working in Hostel B'}),
            'category': forms.Select(),
            'description': forms.Textarea(attrs={
                'placeholder': 'Please provide specific details...',
                'rows': 5,
            }),
            'image': forms.FileInput(), # Added the file input widget
        }
