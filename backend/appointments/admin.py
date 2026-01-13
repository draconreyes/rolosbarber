from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('status', 'service', 'appointment_date')
    search_fields = ('client__username', 'client__email')
    date_hierarchy = 'appointment_date'
