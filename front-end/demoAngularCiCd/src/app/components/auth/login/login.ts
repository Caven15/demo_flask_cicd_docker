import { Component, inject } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService } from '../../../tools/api/auth-service';
import { ActivatedRoute, Router } from '@angular/router';
import { LoginRequest } from '../../../models/auth.model';

@Component({
  selector: 'app-login',
  imports: [ReactiveFormsModule],
  templateUrl: './login.html',
  styleUrl: './login.scss',
})
export class Login {
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);

  loginForm: FormGroup;
  isSubmitting = false;
  error: string | null = null;
  private returnUrl = '/home';

  constructor() {
    this.route.queryParamMap.subscribe((params) => {
      const url = params.get('returnUrl');
      if (url) this.returnUrl = url;
    });

    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required]],
    });
  }

  get f() {
    return this.loginForm.controls;
  }

  onSubmit(): void {
    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      return;
    }

    this.isSubmitting = true;
    this.error = null;

    const payload: LoginRequest = this.loginForm.value;

    this.authService.login(payload).subscribe({
      next: () => {
        this.isSubmitting = false;
        // Ici, l'AuthService a déjà rempli le store + le token.
        // On redirige vers la page d'accueil.
        this.router.navigateByUrl(this.returnUrl);
      },
      error: () => {
        this.isSubmitting = false;
        this.error = 'Identifiants invalides ou erreur serveur.';
      },
    });
  }
}
