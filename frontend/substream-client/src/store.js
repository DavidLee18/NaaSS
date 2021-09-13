import { getAuth, signInWithEmailAndPassword, signOut, createUserWithEmailAndPassword } from 'firebase/auth';
import Vue from 'vue';
import Vuex from 'vuex';
import router from './router';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  modules: {
    auth: {
      state: () => ({
        errorMessage: '',
        user: {},
      }),
      mutations: {
        login(state, user) {
          [state.errorMessage, state.user] = [null, user];
        },
        loginError(state, errorMessage) {
          state.errorMessage = errorMessage;
        },
        logout(state) {
          [state.errorMessage, state.user] = [null, null];
        },
      },
      actions: {
        async login({commit}, {email, password}) {
          try {
            const userCred = await signInWithEmailAndPassword(getAuth(), email, password);
            console.log('successfully logged into firebase');
            commit('login', userCred.user);
            router.push('dashboard');
          } catch (error) {
            console.error(error);

            const errorCode = error.code;
            const errorMessage = errorCode === 'auth/invalid-email' ? 'e-mail 주소가 올바르지 않습니다. 올바른 e-mail 주소를 입력해 주세요.' :
            errorCode === 'auth/user-disabled' ? '귀하는 비활성화된 사용자입니다. 로그인할 수 없습니다.' :
            errorCode === 'auth/user-not-found' ? '입력한 e-mail에 해당하는 계정을 찾을 수 없습니다. 회원가입하신 것이 맞나요?' :
            errorCode === 'auth/wrong-password' ? '비밀번호가 일치하지 않습니다. 비밀번호를 잊어버리셨다면 비밀번호를 재설정하세요.' :
            null;
            commit('loginError', error.code && errorMessage ? errorMessage : error.message);
          }
        },
        async logout({commit}) {
          try {
            await signOut(getAuth());
            commit('logout');
            router.push('login');
          } catch (error) {
            console.error(error);
          }
        },
        async signUp({commit}, {email, password}) {
          try {
            const userCred = await createUserWithEmailAndPassword(getAuth(), email, password);
            commit('login', userCred.user);
          } catch (error) {
            console.error(error);
            commit('loginError', error.message);
          }
        }
      },
      getters: {
        loggedIn: (state) => !state.error && !!state.user,
        errorMessage: (state) => state.errorMessage,
        uid: (state) => state.user ? state.user.uid : null,
        displayName: (state) => state.user ? state.user.displayName : null,
        email: (state) => state.user ? state.user.email : null,
        photoURL: (state) => state.user ? state.user.photoURL : null,
      },
    },
  },
  strict: true, // not in production
});
