import { Routes } from '@angular/router';
import { MsalGuard } from '@azure/msal-angular';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'chat',
    pathMatch: 'full'
  },
  {
    path: 'login-failed',
    loadComponent: () =>
      import('./features/login/page/login-failed.page').then(m => m.LoginFailedPage)
  },
  {
    path: 'chat',
    canActivate: [MsalGuard],
    loadComponent: () =>
      import('./features/chat/page/chat.page').then(m => m.ChatPage)
  },
  {
    path: '**',
    redirectTo: 'chat'
  }
];
