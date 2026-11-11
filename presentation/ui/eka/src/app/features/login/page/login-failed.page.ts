import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-login-failed',
  imports: [RouterLink],
  template: `
    <main>
      <h1>Sign-in failed</h1>
      <p>Authentication could not be completed. Please try again.</p>
      <a routerLink="/chat">Try again</a>
    </main>
  `
})
export class LoginFailedPage {}
