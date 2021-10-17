import Vue from 'vue';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';
import store from './store';

Vue.config.productionTip = false;

// eslint-disable-next-line no-unused-vars
var vm = new Vue({
  router,
  vuetify,
  store,
  render: (h) => h(App),
}).$mount('#app');
