import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { LoginRequest } from '../../models/models';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  credentials: LoginRequest = {
    username: '',
    password: ''
  };
  error = '';

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  onSubmit(): void {
    this.error = '';
    this.authService.login(this.credentials).subscribe({
      next: () => {
        // Load user profile first, then redirect based on role
        this.authService.getProfile().subscribe({
          next: (user) => {
            if (user.role === 'admin') {
              this.router.navigate(['/appointments/today']);
            } else {
              this.router.navigate(['/appointments/my_appointments']);
            }
          },
          error: (err) => {
            console.error('Error loading profile:', err);
            this.router.navigate(['/login']);
          }
        });
      },
      error: (err) => {
        this.error = 'Invalid credentials';
        console.error(err);
      }
    });
  }
}
