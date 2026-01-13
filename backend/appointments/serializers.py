from rest_framework import serializers
from .models import Appointment
from users.serializers import UserSerializer


class AppointmentSerializer(serializers.ModelSerializer):
    client_details = UserSerializer(source='client', read_only=True)
    
    class Meta:
        model = Appointment
        fields = ('id', 'client', 'client_details', 'service', 'appointment_date', 
                  'appointment_time', 'status', 'notes', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at', 'client')
    
    def validate(self, data):
        appointment_date = data.get('appointment_date')
        appointment_time = data.get('appointment_time')
        
        if self.instance:
            existing = Appointment.objects.filter(
                appointment_date=appointment_date,
                appointment_time=appointment_time
            ).exclude(id=self.instance.id)
        else:
            existing = Appointment.objects.filter(
                appointment_date=appointment_date,
                appointment_time=appointment_time
            )
        
        if existing.exists():
            raise serializers.ValidationError("This time slot is already booked")
        
        return data


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('service', 'appointment_date', 'appointment_time', 'notes')
