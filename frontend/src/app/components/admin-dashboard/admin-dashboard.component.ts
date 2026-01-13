import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AppointmentService } from '../../services/appointment.service';
import { AuthService } from '../../services/auth.service';
import { Appointment } from '../../models/models';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-dashboard.component.html',
  styleUrls: ['./admin-dashboard.component.css']
})
export class AdminDashboardComponent implements OnInit {
  todayAppointments: Appointment[] = [];
  selectedDate: string = '';
  showingToday: boolean = true;
  expandedAppointmentId: number | null = null;

  constructor(
    private appointmentService: AppointmentService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadTodayAppointments();
  }

  loadTodayAppointments(): void {
    this.showingToday = true;
    this.selectedDate = '';
    this.appointmentService.getTodayAppointments().subscribe({
      next: (data) => this.todayAppointments = data,
      error: (err) => console.error(err)
    });
  }

  onDateChange(): void {
    if (this.selectedDate) {
      this.showingToday = false;
      this.appointmentService.getAppointmentsByDate(this.selectedDate).subscribe({
        next: (data) => this.todayAppointments = data,
        error: (err) => console.error(err)
      });
    }
  }

  toggleDetails(appointmentId: number): void {
    this.expandedAppointmentId = this.expandedAppointmentId === appointmentId ? null : appointmentId;
  }

  confirmAppointment(appointment: Appointment): void {
    if (appointment.id) {
      this.appointmentService.updateAppointmentStatus(appointment.id, 'confirmed').subscribe({
        next: (updated) => {
          appointment.status = updated.status;
        },
        error: (err) => console.error(err)
      });
    }
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

  viewAllAppointments(): void {
    this.router.navigate(['/appointments']);
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
