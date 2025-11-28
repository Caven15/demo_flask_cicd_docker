import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService } from '../../../tools/api/auth-service';
import { Router } from '@angular/router';
import { RegisterRequest } from '../../../models/auth.model';

@Component({
  selector: 'app-register',
  imports: [ReactiveFormsModule],
  templateUrl: './register.html',
  styleUrl: './register.scss',
})
export class Register {
  registerForm: FormGroup;
  isSubmitting = false;
  error: string | null = null;
  successMessage: string | null = null;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
  ) {
    // Formulaire d'inscription
    this.registerForm = this.fb.group(
      {
        email: ['', [Validators.required, Validators.email]],
        password: ['', [Validators.required, Validators.minLength(4)]],
        confirmPassword: ['', [Validators.required]],
      },
      {
        // Validator de groupe pour vérifier que password == confirmPassword
        validators: (group) => {
          const pass = group.get('password')?.value;
          const confirm = group.get('confirmPassword')?.value;

          if (pass && confirm && pass !== confirm) {
            group.get('confirmPassword')?.setErrors({ passwordMismatch: true });
          } else {
            // S'il n'y a pas d'autre erreur, on nettoie passwordMismatch
            const errors = group.get('confirmPassword')?.errors;
            if (errors && errors['passwordMismatch']) {
              delete errors['passwordMismatch'];
              if (Object.keys(errors).length === 0) {
                group.get('confirmPassword')?.setErrors(null);
              } else {
                group.get('confirmPassword')?.setErrors(errors);
              }
            }
          }

          return null;
        },
      },
    );
  }

  get f() {
    return this.registerForm.controls;
  }

  onSubmit(): void {
    if (this.registerForm.invalid) {
      this.registerForm.markAllAsTouched();
      return;
    }

    this.isSubmitting = true;
    this.error = null;
    this.successMessage = null;

    const payload: RegisterRequest = this.registerForm.value;

    this.authService.register(payload).subscribe({
      next: (res) => {
        this.isSubmitting = false;
        this.successMessage = res.message || 'Inscription réussie.';

        // Option simple : rediriger vers la page de login
        this.router.navigate(['/login']);
      },
      error: (err) => {
        console.error(err);
        this.isSubmitting = false;

        // Gestion d'erreur simple
        if (err.status === 409) {
          this.error = "Un utilisateur avec cet email existe déjà.";
        } else if (err.error?.errors) {
          // Cas où le back renvoie { errors: {...} }
          this.error = 'Données invalides, vérifiez le formulaire.';
        } else {
          this.error = "Erreur lors de l'inscription. Réessayez plus tard.";
        }
      },
    });
  }
}
