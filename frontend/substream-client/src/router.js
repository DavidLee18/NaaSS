import Vue from 'vue';
import VueRouter from 'vue-router';
import Dashboard from './components/Dashboard.vue';
import Login from './components/Login.vue';
import store from './store';
import nginxTrip from './components/NGINX_Trip.vue';
import signup from './components/SignUp.vue';
import notFound from './components/NotFound.vue';

Vue.use(VueRouter);

const router = new VueRouter({
  mode: 'history',
  base: '/app/',
  routes: [
    {
      path: '/',
      redirect: '/login',
      beforeEnter: noAuthGuard,
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: Dashboard,
      beforeEnter: authGuard,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      beforeEnter: noAuthGuard,
    },
    {
      path: '/nginx-trip',
      name: 'NGINX Trip',
      component: nginxTrip,
      beforeEnter: authGuard,
    },
    {
      path: '/sign-up',
      name: 'SignUp',
      component: signup,
      beforeEnter: noAuthGuard,
    },
    {
      path: '**',
      component: notFound,
    },
  ],
});

const authGuard = (to, from, next) => {
  const loggedIn = store.getters.loggedIn;

  if (!loggedIn && to.path !== '/login') next('/login');
  else next();
};

const noAuthGuard = (to, from, next) => {
  const loggedIn = store.getters.loggedIn;

  if (loggedIn && to.path === '/login') next('/dashboard');
  else next();
};

export default router;
