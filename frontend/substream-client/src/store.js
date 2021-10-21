import Vue from 'vue';
import Vuex from 'vuex';
import router from './router';
import * as nimrod from './nimrod';

Vue.use(Vuex);

const auth = {
  state: () => ({
    userProfile: null,
  }),
  mutations: {
    login(state, profile) { state.userProfile = profile; },
    logout(state) { state.userProfile = null; },
  },
  actions: {
    async login({ commit, dispatch }, { username, password }) {
      try {
        const res = await nimrod.login(username, password);
        if(res && res.status === 200) {
          const userProfile = res.data;
          console.log('successfully logged in');
          commit('login', userProfile);
          router.push('dashboard');
        }
      } catch (error) {
        console.error(error);
        await dispatch('setError', error.message);
      }
    },
    async logout({ commit, dispatch }) {
      try {
        const loggedOut = await nimrod.logout();
        if (loggedOut) {
          commit('logout');
          router.push('login');
        }
        else commit('loginError', 'logout failed');
      } catch (error) {
        console.error(error);
        await dispatch('setError', error.message);
      }
    },
    async signUp({ commit, dispatch }, { username, email, password }) {
      try {
        const res = await nimrod.createUser(username, email, password);
        if(res && res.status === 200) {
          const userProfile = res.data;
          commit('login', userProfile);
        }
      } catch (error) {
        console.error(error);
        await dispatch('setError', error.message);
      }
    }
  },
  getters: {
    loggedIn: (state) => !state.errorMessage && !!state.userProfile,
    userName: (state) => state.userProfile ? state.userProfile.user.username : null,
    email: (state) => state.userProfile ? state.userProfile.user.email : null,
    firstName: (state) => state.userProfile ? state.userProfile.user.first_name : null,
    lastName: (state) => state.userProfile ? state.userProfile.user.last_name : null,
  },
};

const error = {
  state: () => ({
    errorOccured: false,
    errorMessage: '',
    errorHtml: '',
  }),
  mutations: {
    htmlError(state, html) {
      [state.errorOccured, state.errorMessage, state.errorHtml] = [true, null, html];
    },
    error(state, errorMessage) {
      [state.errorOccured, state.errorMessage, state.errorHtml] = [true, errorMessage, null];
    },
    noError(state) {
      [state.errorOccured, state.errorMessage, state.errorHtml] = [false, null, null];
    },
  },
  actions: {
    async setError({ commit }, errorString) {
      if(errorString.startsWith('<!DOCTYPE html>')) commit('htmlError', errorString);
      else commit('error', errorString);
    },
    async unsetError({ commit }) { commit('noError'); },
  },
  getters: {
    errorOccured: state => state.errorOccured,
    errorMessage: state => state.errorMessage,
    errorHtml: state => state.errorHtml
  },
};

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  modules: { auth, error }
});
