/* eslint-disable no-extra-boolean-cast */
/* eslint-disable no-unused-vars */
import { getAuth, signInWithEmailAndPassword, signOut } from 'firebase/auth'
import Vue from 'vue'
import Vuex from 'vuex'
import router from '../router'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    auth: {
      state: () => ({
        error: false,
        uid: ''
      }),
      mutations: {
        login(state, uid) { [state.error, state.uid] = [false, uid] },
        loginError({error}) { error = true },
        logout({error, uid}) { [error, uid] = [false, null] }
      },
      actions: {
        async login({commit, dispatch}, {email, password}) {
          try {
            const userCred = await signInWithEmailAndPassword(getAuth(), email, password);
            commit('login', userCred.user.uid);
            router.push('/');
          } catch (error) {
            console.error(JSON.stringify(error));
            commit('loginError');
          }
        },
        async logout({commit}) {
          await signOut(getAuth());
          commit('logout');
          router.push('login');
        }
      },
      getters: {
        loggedIn: ({error, uid}) => !error && !!uid,
        uid: ({uid}) => !!uid ? uid : null
      }
    }
  },
  strict: true //not in production
})
