import * as nimrod from '../../nimrod';
import router from '../../router';

export default {
    state: () => ({
      user: null,
      profile: null,
      loggedIn: false
    }),
    mutations: {
        getMyInfo(state, user) { [state.user, state.loggedIn] = [user, true]; },
        getMyProfile(state, profile) { [state.profile, state.loggedIn] = [profile, true]; },
        login(state) { state.loggedIn = true; },
        logout(state) { [state.user, state.profile, state.loggedIn] = [null, null, false]; },
    },
    actions: {
      async login({ commit, dispatch }, { email, password }) {
        try {
          const res = await nimrod.login(email, password);
          if(res && res.status === 200) {
            console.log('successfully logged in');
            commit('login');
            await dispatch('getMyInfo');
            await dispatch('getMyProfile');
            router.push('dashboard');
          }
        } catch (error) {
          console.error(error);
          commit('logout');
          await dispatch('setError', error.message);
        }
      },
      async logout({ commit }) {
        const loggedOut = await nimrod.logout();
        if(loggedOut) {
          commit('logout');
          router.push('login');
        }
      },
      async createUserAndLogin({ commit, dispatch }, { email, password }) {
        try {
          const res = await nimrod.createUser(email, password);
          if(res && res.status === 201) {
            const user = res.data;
            commit('getMyInfo', user);
            const res2 = await nimrod.login(email, password);
            if(res2 && res2.status === 200) {
                commit('login');
                await dispatch('getMyInfo');
                await dispatch('getMyProfile');
            }
          }
        } catch (error) {
          console.error(error);
          commit('logout');
          await dispatch('setError', error.message);
        }
      },
      async getMyInfo({ commit, dispatch }) {
        try {
          const res = await nimrod.getMyInfo();
          if (res && res.status === 200) {
            const info = res.data;
            commit('getMyInfo', info);
          }
        } catch (error) {
          console.error(error);
          await dispatch('setError', error.message);
        }
      },
      async getMyProfile({ commit, dispatch, getters }) {
        try {
          await dispatch('getMyInfo');
          const res = await nimrod.getProfiles();
          if (res && res.status === 200) {
            const profiles = res.data;
            const userId = getters.userId;
            const profile = profiles.filter(p => p.owner_id === userId);
            if (profile.length > 0) commit('getMyProfile', profile[0]);
          }
        } catch (error) {
          console.error(error);
          await dispatch('setError', error.message);
        }
      },
      async createProfile({ commit, dispatch, getters }, profile) {
        try {
          const res = await nimrod.createProfile(getters.userId, profile);
          if (res && res.status === 201) {
            const createdProfile = res.data;
            commit('getMyProfile', createdProfile);
          }
        } catch (error) {
          console.error(error);
          await dispatch('setError', error.message);
        }
      },
      async editProfile({ state, dispatch, getters }, profile) {
        try {
          const edited = await nimrod.editProfile(getters.profileId, { ...state.profile, ...profile });
          if (edited) await dispatch('getMyProfile');
        } catch (error) {
          console.error(error);
          await dispatch('setError', error.message);
        }
      }
    },
    getters: {
      loggedIn: state => state.loggedIn,
      name: state => state.profile ? state.profile.name : null,
      alias: state => state.profile ? state.profile.alias : null,
      email: state => state.user ? state.user.email : null,
      userId: state => state.user ? state.user.id : null,
      profileId: state => state.profile ? state.profile.id : null,
      preferDark: state => state.profile ? state.profile.prefer_dark : false
    },
  };