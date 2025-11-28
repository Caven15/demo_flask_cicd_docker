import { Component, inject, signal } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { AuthStore } from './tools/store/auth-store';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  private router = inject(Router);
  private authStore = inject(AuthStore);

  // signal exposé pour le template
  user = this.authStore.user;

  goTo(path: string) {
    this.router.navigateByUrl(path);
  }
}
