import { inject } from '@angular/core';
import {
  HttpInterceptorFn,
} from '@angular/common/http';
import { TokenService } from '../utils/token-service';

// Interceptor *fonctionnel* (nouveau style Angular)
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const tokenService = inject(TokenService);
  const token = tokenService.getToken();

  if (!token) {
    // Pas de token => on laisse passer la requête telle quelle
    return next(req);
  }

  const cloned = req.clone({
    setHeaders: {
      Authorization: `Bearer ${token}`,
    },
  });

  return next(cloned);
};
