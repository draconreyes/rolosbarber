from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime, time
import logging
from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentCreateSerializer
from .permissions import IsAdminUser, IsOwnerOrAdmin

logger = logging.getLogger(__name__)


class AppointmentListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        logger.info(f"GET /appointments/ - User: {user.username}")
        logger.info(f"GET /appointments/ - User Rol: {user.role}")
        logger.info(f"  - role: {user.role}")
        logger.info(f"  - is_admin: {user.is_admin}")
        
        if user.is_admin:
            logger.info(f"  - Admin access: returning ALL appointments")
            appointments = Appointment.objects.all()
        else:
            logger.info(f"  - Client access: returning only user's appointments")
            appointments = Appointment.objects.filter(client=user)
        
        serializer = AppointmentSerializer(appointments, many=True)
        logger.info(f"  - Returning {len(serializer.data)} appointments")
        return Response(serializer.data)
    
    def post(self, request):
        logger.info(f"POST /appointments/ - User: {request.user.username}")
        serializer = AppointmentCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(client=request.user)
            logger.info(f"  - Appointment created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        logger.error(f"  - Validation errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        try:
            appointment = Appointment.objects.get(pk=pk)
            if user.is_admin or appointment.client == user:
                return appointment
            return None
        except Appointment.DoesNotExist:
            return None
    
    def get(self, request, pk):
        logger.info(f"GET /appointments/{pk}/ - User: {request.user.username}")
        appointment = self.get_object(pk, request.user)
        if not appointment:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)
    
    def patch(self, request, pk):
        logger.info(f"PATCH /appointments/{pk}/ - User: {request.user.username}")
        logger.info(f"  - Data: {request.data}")
        appointment = self.get_object(pk, request.user)
        if not appointment:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Only allow status changes
        allowed_fields = ['status']
        filtered_data = {k: v for k, v in request.data.items() if k in allowed_fields}
        
        serializer = AppointmentSerializer(appointment, data=filtered_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"  - Appointment updated successfully")
            return Response(serializer.data)
        
        logger.error(f"  - Validation errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        appointment = self.get_object(pk, request.user)
        if not appointment:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyAppointmentsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        logger.info(f"GET /appointments/my_appointments/ - User: {request.user.username}")
        appointments = Appointment.objects.filter(client=request.user)
        serializer = AppointmentSerializer(appointments, many=True)
        logger.info(f"  - Returning {len(serializer.data)} appointments")
        return Response(serializer.data)


class TodayAppointmentsView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        logger.info(f"GET /appointments/today/ - User: {request.user.username}")
        logger.info(f"  - role: {request.user.role}")
        logger.info(f"  - is_admin: {request.user.is_admin}")
        
        today = timezone.now().date()
        appointments = Appointment.objects.filter(appointment_date=today)
        serializer = AppointmentSerializer(appointments, many=True)
        
        logger.info(f"  - Found {len(serializer.data)} appointments for today")
        return Response(serializer.data)


class AppointmentsByDateView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        logger.info(f"GET /appointments/by_date/ - User: {request.user.username}")
        logger.info(f"  - role: {request.user.role}")
        logger.info(f"  - is_admin: {request.user.is_admin}")
        
        date_str = request.query_params.get('date')
        if not date_str:
            logger.error("  - Missing date parameter")
            return Response({'error': 'Date parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            appointments = Appointment.objects.filter(appointment_date=date_obj)
            serializer = AppointmentSerializer(appointments, many=True)
            
            logger.info(f"  - Found {len(serializer.data)} appointments for {date_str}")
            return Response(serializer.data)
        except ValueError:
            logger.error(f"  - Invalid date format: {date_str}")
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)


class AvailableSlotsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        logger.info(f"GET /appointments/available_slots/ - User: {request.user.username}")
        date_str = request.query_params.get('date')
        
        if not date_str:
            return Response({'error': 'Date parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate time slots from 8 AM to 8 PM (every hour)
        start_hour = 8
        end_hour = 20
        all_slots = []
        
        for hour in range(start_hour, end_hour + 1):
            slot_time = time(hour, 0)
            all_slots.append(slot_time.strftime('%H:%M'))
        
        # Get booked slots for the date
        booked_appointments = Appointment.objects.filter(
            appointment_date=date_obj
        ).values_list('appointment_time', flat=True)
        
        booked_slots = [t.strftime('%H:%M') for t in booked_appointments]
        available_slots = [slot for slot in all_slots if slot not in booked_slots]
        
        logger.info(f"  - Date: {date_str}, Available: {len(available_slots)}, Booked: {len(booked_slots)}")
        
        return Response({
            'date': date_str,
            'available_slots': available_slots,
            'booked_slots': booked_slots
        })
