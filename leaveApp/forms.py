from django import forms
from django.core.exceptions import ValidationError

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