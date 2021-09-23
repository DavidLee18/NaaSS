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

export const handleError = (error) => {
  if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error(`\\response data: ${JSON.stringify(error.response.data)}`);
      console.error(`\\response status: ${error.response.statusText} (${error.response.status})`);
      console.error(`\\response headers: ${JSON.stringify(error.response.headers)}`);
  } else if (error.request) {
      // The request was made but no response was received
      // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
      // http.ClientRequest in node.js
      console.error(`\\request: ${JSON.stringify(error.request)}`);
  } else {
      // Something happened in setting up the request that triggered an Error
      console.error(`\\${error.message}`);
  }
  console.error(`\\${JSON.stringify(error.config)}`);
};