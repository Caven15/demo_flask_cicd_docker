import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import {
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  User,
} from '../../models/auth.model';
import { TokenService } from '../utils/token-service';
import { AuthStore } from '../store/auth-store';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private http = inject(HttpClient);
  private tokenService = inject(TokenService);
  private authStore = inject(AuthStore);

  private readonly baseUrl = `http://localhost:5000/api/auth`;

  login(payload: LoginRequest): Observable<LoginResponse> {
    return this.http
      .post<LoginResponse>(`${this.baseUrl}/login`, payload)
      .pipe(
        tap((res) => {
          // 1) on stocke le token
          this.tokenService.setToken(res.access_token);
          // 2) on stocke l'utilisateur dans le store (signal)
          this.authStore.setUser(res.user);
        }),
      );
  }

  register(payload: RegisterRequest): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/register`, payload);
  }

  logout(): void {
    this.tokenService.clearToken();
    this.authStore.clear();
  }

  get currentUser(): User | null {
    return this.authStore.user();
  }

  get isLoggedIn(): boolean {
    return this.authStore.isLoggedIn();
  }
}
