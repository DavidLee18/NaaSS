import Vue from 'vue';
import Vuex from 'vuex';

import auth from './modules/auth';
import error from './modules/error';
import dark from './modules/dark';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  modules: { auth, error, dark }
});
