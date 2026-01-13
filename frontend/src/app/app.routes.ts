import { Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { AppointmentListComponent } from './components/appointment-list/appointment-list.component';
import { AppointmentFormComponent } from './components/appointment-form/appointment-form.component';
import { AdminDashboardComponent } from './components/admin-dashboard/admin-dashboard.component';
import { authGuard, adminGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'appointments/my_appointments', component: AppointmentListComponent, canActivate: [authGuard] },
  { path: 'appointments/today', component: AdminDashboardComponent, canActivate: [adminGuard] },
  { path: 'appointments/new', component: AppointmentFormComponent, canActivate: [authGuard] },
  { path: 'appointments', component: AppointmentListComponent, canActivate: [authGuard] },
  { path: '**', redirectTo: '/login' }
];
