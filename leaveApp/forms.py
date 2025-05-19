from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class LeaveRequestForm(forms.Form):
    LEAVE_CHOICES = [
        ('Annual', 'Annual'),
        ('Sick', 'Sick'),
        ('Other', 'Other'),
    ]
    leave_type = forms.ChoiceField(choices=LEAVE_CHOICES, label='Leave Type')
    attachment = forms.FileField(
        label='Attachment (Image or PDF)',
        widget=forms.ClearableFileInput(attrs={'accept': 'image/*,application/pdf'})
    )

    def clean_attachment(self):
        file = self.cleaned_data.get('attachment')
        if file:
            valid_types = ['image/jpeg', 'image/png', 'application/pdf']
            if file.content_type not in valid_types:
                raise ValidationError('Please upload an image or PDF file only.')
        return file



class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    user_type = forms.ChoiceField(choices=[
        ('user', 'User'),
        ('staff', 'Staff'),
    ], label='User Type')

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'user_type']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        # Check if the passwords match
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data