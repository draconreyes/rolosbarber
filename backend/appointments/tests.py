from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date, time
from .models import Appointment

User = get_user_model()


class AppointmentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='client1',
            password='pass123',
            role='client'
        )
        self.admin = User.objects.create_user(
            username='admin1',
            password='pass123',
            role='admin'
        )
    
    def test_create_appointment(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'service': 'haircut',
            'appointment_date': '2025-12-31',
            'appointment_time': '10:00:00',
            'notes': 'Test appointment'
        }
        response = self.client.post('/api/appointments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 1)
    
    def test_client_can_view_own_appointments(self):
        self.client.force_authenticate(user=self.user)
        Appointment.objects.create(
            client=self.user,
            service='haircut',
            appointment_date=date(2025, 12, 31),
            appointment_time=time(10, 0)
        )
        response = self.client.get('/api/appointments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_admin_can_view_all_appointments(self):
        self.client.force_authenticate(user=self.admin)
        Appointment.objects.create(
            client=self.user,
            service='haircut',
            appointment_date=date(2025, 12, 31),
            appointment_time=time(10, 0)
        )
        response = self.client.get('/api/appointments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_prevent_double_booking(self):
        self.client.force_authenticate(user=self.user)
        Appointment.objects.create(
            client=self.user,
            service='haircut',
            appointment_date=date(2025, 12, 31),
            appointment_time=time(10, 0)
        )
        data = {
            'service': 'beard',
            'appointment_date': '2025-12-31',
            'appointment_time': '10:00:00'
        }
        response = self.client.post('/api/appointments/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
