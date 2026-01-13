from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='client'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.role, 'client')
        self.assertTrue(user.check_password('testpass123'))
    
    def test_register_endpoint(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'phone': '1234567890'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_login_endpoint(self):
        User.objects.create_user(
            username='loginuser',
            password='loginpass123'
        )
        data = {
            'username': 'loginuser',
            'password': 'loginpass123'
        }
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
