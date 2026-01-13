import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AppointmentService } from '../../services/appointment.service';
import { AuthService } from '../../services/auth.service';
import { Appointment } from '../../models/models';

@Component({
  selector: 'app-appointment-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './appointment-list.component.html',
  styleUrls: ['./appointment-list.component.css']
})
export class AppointmentListComponent implements OnInit {
  appointments: Appointment[] = [];
  isAdmin = false;

  constructor(
    private appointmentService: AppointmentService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.isAdmin = this.authService.isAdmin();
    this.loadAppointments();
  }

  loadAppointments(): void {
    if (this.isAdmin) {
      this.appointmentService.getAppointments().subscribe({
        next: (data) => this.appointments = data,
        error: (err) => console.error(err)
      });
    } else {
      this.appointmentService.getMyAppointments().subscribe({
        next: (data) => this.appointments = data,
        error: (err) => console.error(err)
      });
    }
  }

  createAppointment(): void {
    this.router.navigate(['/appointments/new']);
  }

  cancelAppointment(appointment: Appointment): void {
    if (appointment.id && confirm('Are you sure you want to cancel this appointment?')) {
      this.appointmentService.updateAppointmentStatus(appointment.id, 'canceled').subscribe({
        next: (updated) => {
          appointment.status = updated.status;
        },
        error: (err) => console.error(err)
      });
    }
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
