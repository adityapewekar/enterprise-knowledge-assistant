import { Routes } from '@angular/router';

export const routes: Routes = [
      {
    path: '',
    redirectTo: 'chat',
    pathMatch: 'full'
  },
  {
    path: 'chat',
    loadComponent: () =>
      import('./features/chat/page/chat.page').then(m => m.ChatPage)
  },
  {
    path: '**',
    redirectTo: 'chat'
  }
 ];
