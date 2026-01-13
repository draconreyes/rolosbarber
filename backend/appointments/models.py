from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

User = get_user_model()


class Appointment(models.Model):
    SERVICE_CHOICES = (
        ('haircut', 'Haircut'),
        ('beard', 'Beard'),
        ('combo', 'Combo'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    )
    
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['appointment_date', 'appointment_time']
        unique_together = ['appointment_date', 'appointment_time']
    
    def __str__(self):
        return f"{self.client.username} - {self.service} on {self.appointment_date} at {self.appointment_time}"
    
    def clean(self):
        if self.appointment_date and self.appointment_time:
            appointment_datetime = timezone.datetime.combine(self.appointment_date, self.appointment_time)
            if timezone.make_aware(appointment_datetime) < timezone.now():
                raise ValidationError("Cannot create appointments in the past")
