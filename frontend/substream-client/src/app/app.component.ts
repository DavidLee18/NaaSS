import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'substream-client';
  loggedIn = true;
  routes = [
    { path: '/', label: '구독', icon: 'subscriptions' },
    { path: '/', label: 'Training' }
  ];

  readonly logout = () => this.loggedIn = false;
}
