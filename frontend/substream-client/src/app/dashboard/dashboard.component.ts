import { Component, OnInit } from '@angular/core';
import { NimrodService } from '../nimrod.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  readonly loggedIn = this._nimrod.loggedIn;
  readonly routes = this._nimrod.routeNames;

  readonly logout = () => this._nimrod.logout();

  constructor(private _nimrod: NimrodService) {}
  ngOnInit() {}
}
