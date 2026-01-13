import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AppointmentService } from '../../services/appointment.service';
import { Appointment } from '../../models/models';

@Component({
  selector: 'app-appointment-form',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './appointment-form.component.html',
  styleUrls: ['./appointment-form.component.css']
})
export class AppointmentFormComponent {
  appointment: Appointment = {
    service: 'haircut',
    appointment_date: '',
    appointment_time: '',
    notes: ''
  };
  availableSlots: string[] = [];
  selectedDate: string = '';
  error = '';
  success = false;
  loadingSlots = false;

  constructor(
    private appointmentService: AppointmentService,
    private router: Router
  ) {}

  onDateChange(): void {
    if (this.appointment.appointment_date) {
      this.loadingSlots = true;
      this.appointmentService.getAvailableSlots(this.appointment.appointment_date).subscribe({
        next: (data) => {
          this.availableSlots = data.available_slots;
          this.loadingSlots = false;
          this.appointment.appointment_time = '';
        },
        error: (err) => {
          console.error(err);
          this.loadingSlots = false;
        }
      });
    }
  }

  onSubmit(): void {
    this.error = '';
    this.appointmentService.createAppointment(this.appointment).subscribe({
      next: () => {
        this.success = true;
        setTimeout(() => {
          this.router.navigate(['/appointments']);
        }, 2000);
      },
      error: (err) => {
        this.error = err.error?.non_field_errors?.[0] || 'Failed to create appointment';
        console.error(err);
      }
    });
  }
}
