import { Injectable, signal, computed } from '@angular/core';
import { User } from '../../models/auth.model';

// Petit store maison basé sur les signals Angular.
// Il conserve l'utilisateur connecté et expose quelques helpers.
@Injectable({
  providedIn: 'root',
})
export class AuthStore {
  // Signal qui contient l'utilisateur courant (ou null)
  private readonly _user = signal<User | null>(null);

  // Lecture publique (readonly)
  readonly user = computed(() => this._user());

  // Computed pratique pour savoir si quelqu'un est connecté
  readonly isLoggedIn = computed(() => this._user() !== null);

  // Met à jour l'utilisateur (appelé après un login)
  setUser(user: User | null): void {
    this._user.set(user);
  }

  // Reset (logout)
  clear(): void {
    this._user.set(null);
  }
}
