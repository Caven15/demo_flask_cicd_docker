import { Component, computed, inject } from '@angular/core';
import { AuthStore } from '../../tools/store/auth-store';

@Component({
  selector: 'app-home',
  imports: [],
  templateUrl: './home.html',
  styleUrl: './home.scss',
})
export class Home {
  private authStore = inject(AuthStore);

  // on expose le user via un computed pratique pour le template
  readonly user = computed(() => this.authStore.user());

  // message de bienvenue (si pas connecté, message générique)
  readonly welcomeMessage = computed(() => {
    const u = this.user();
    if (!u) {
      return "Bienvenue sur la démo Fullstack CI/CD (non connecté)";
    }
    return `Bienvenue ${u.email} 👋`;
  });
}
