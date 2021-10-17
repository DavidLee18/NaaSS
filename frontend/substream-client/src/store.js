import Vue from 'vue';
import Vuex from 'vuex';
import router from './router';
import * as nimrod from './nimrod';

Vue.use(Vuex);

const auth = {
  state: () => ({
    errorMessage: '',
    userProfile: null,
  }),
  mutations: {
    login(state, profile) {
      [state.errorMessage, state.userProfile] = [null, profile];
    },
    loginError(state, errorMessage) {
      state.errorMessage = errorMessage;
    },
    logout(state) {
      [state.errorMessage, state.userProfile] = [null, null];
    },
  },
  actions: {
    async login({ commit }, { username, password }) {
      try {
        const res = await nimrod.login(username, password);
        if(!res || res.status !== 200) throw Error('login request failed for an unknown reason');
        else {
          const userProfile = res.data;
          console.log('successfully logged in: ' + JSON.stringify(userProfile));
          commit('login', userProfile);
          router.push('dashboard');
        }
      } catch (error) {
        console.error(error);
        commit('loginError', error.message);
      }
    },
    async logout({ commit }) {
      try {
        const loggedOut = await nimrod.logout();
        if (loggedOut) {
          commit('logout');
          router.push('login');
        }
        else commit('loginError', 'logout failed');
      } catch (error) {
        console.error(error);
      }
    },
    async signUp({ commit }, { username, email, password }) {
      try {
        const res = await nimrod.createUser(username, email, password);
        if(!res || res.status !== 200) throw Error('createUser request failed for an unknown reason');
        else {
          const userProfile = res.data;
          commit('login', userProfile);
        }
      } catch (error) {
        console.error(error);
        commit('loginError', error.message);
      }
    }
  },
  getters: {
    loggedIn: (state) => !state.errorMessage && !!state.userProfile,
    errorMessage: (state) => state.errorMessage,
    userName: (state) => state.userProfile ? state.userProfile.user.username : null,
    email: (state) => state.userProfile ? state.userProfile.user.email : null,
    firstName: (state) => state.userProfile ? state.userProfile.user.first_name : null,
    lastName: (state) => state.userProfile ? state.userProfile.user.last_name : null,
  },
};

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  modules: { auth }
});
