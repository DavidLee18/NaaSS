import {getAuth, onAuthStateChanged} from '@firebase/auth';
import router from './router';
import store from './store';

export const authGuard = (to, from, next) => whenAuthChanges(next, () => {
  if (to.path !== 'login') next('login');
});

export const noAuthGuard = (to, from, next) => whenAuthChanges(() => {
  if (to.path === '/login') next('dashboard');
}, next);

const whenAuthChanges = (whenOn, whenOff) =>
  onAuthStateChanged(getAuth(), (user) => {
    if (user) whenOn(); else whenOff();
  }, console.error);

export const logInSafely = (user) => {
  store.commit('login', user);
  router.push('dashboard');
};

export const logoutSafely = () => {
  store.commit('logout');
  router.push('login');
};
