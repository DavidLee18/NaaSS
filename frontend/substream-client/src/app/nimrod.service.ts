import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { from, Observable, of, pipe } from 'rxjs';
import { map, tap } from "rxjs/operators";

const routeNames = [
  { path: '/', label: '구독', icon: 'subscriptions' },
  { path: '/', label: 'Training' }
];

@Injectable({
  providedIn: 'root'
})
export class NimrodService {

  constructor(private _http: HttpClient) { }

  get loggedIn() { return of(true); }

  logout() { this.loggedIn.pipe(tap(l => console.log(`logging out, changing loggedIn state from ${l} to ${!l}`))); }

  get routeNames() { return this.loggedIn.pipe(map(l => l ? routeNames : [])); }
}
