from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class LeaveRequest(models.Model):
    LEAVE_CHOICES = [
        ('Annual', 'Annual'),
        ('Sick', 'Sick'),
        ('Other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_CHOICES)
    attachment = models.FileField(upload_to='leave_attachments/')
    status = models.CharField(max_length=10, default='Pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.leave_type} - {self.status}"