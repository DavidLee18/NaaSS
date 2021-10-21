import router from './router';
import store from './store';

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

      store.dispatch('setError', JSON.stringify(error.response.data));
  } else if (error.request) {
      // The request was made but no response was received
      // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
      // http.ClientRequest in node.js
      console.error(`\\request: ${JSON.stringify(error.request)}`);

      store.dispatch('setError', error.message);
  } else {
      // Something happened in setting up the request that triggered an Error
      console.error(`\\message: ${error.message}`);

      store.dispatch('setError', error.message);
  }
  console.error(`\\config: ${JSON.stringify(error.config)}`);
};