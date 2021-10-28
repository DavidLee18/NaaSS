import * as nimrod from '../../nimrod';
import router from '../../router';

export default {
    state: () => ({
      user: null,
      profile: null,
      token: null
    }),
    mutations: {
        getMyInfo(state, user) { state.user = user; },
        getMyProfile(state, profile) { state.profile = profile },
        login(state, token) { state.token = token; },
        logout(state) { [state.user, state.profile, state.token] = [null, null, null]; },
    },
    actions: {
      async login({ commit, dispatch }, { email, password }) {
        try {
          const res = await nimrod.login(email, password);
          if(res && res.status === 200) {
            const token = res.data.access_token;
            console.log('successfully logged in');
            commit('login', token);
            router.push('dashboard');
          }
        } catch (error) {
          console.error(error);
          await dispatch('setError', error.message);
        }
      },
      async logout({ commit }) {
          commit('logout');
          router.push('login');
      },
      async signUp({ commit, dispatch }, { email, password }) {
        try {
          const res = await nimrod.createUser(email, password);
          if(res && res.status === 201) {
            const user = res.data;
            commit('getMyInfo', user);
            const res2 = await nimrod.login(email, password);
            if(res && res.status === 200) {
                const token = res2.data.access_token;
                commit('login', token);
            }
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