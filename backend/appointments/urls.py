from django.urls import path
from .views import (
    AppointmentListCreateView,
    AppointmentDetailView,
    MyAppointmentsView,
    TodayAppointmentsView,
    AppointmentsByDateView,
    AvailableSlotsView
)

urlpatterns = [
    path('appointments/', AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('appointments/my_appointments/', MyAppointmentsView.as_view(), name='my-appointments'),
    path('appointments/today/', TodayAppointmentsView.as_view(), name='today-appointments'),
    path('appointments/by_date/', AppointmentsByDateView.as_view(), name='appointments-by-date'),
    path('appointments/available_slots/', AvailableSlotsView.as_view(), name='available-slots'),
]
