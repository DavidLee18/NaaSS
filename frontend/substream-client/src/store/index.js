import Vue from 'vue';
import Vuex from 'vuex';

import auth from './modules/auth'; //사용자 인증 및 프로필 관리 모듈
import error from './modules/error'; //에러가 발생했을 때 사용자에게 적절히 보여주기 위한 모듈
import dark from './modules/dark'; //시스템 다크모드와 사용자의 다크모드 선호도를 읽고 반영 및 수정을 하기 위한 모듈

Vue.use(Vuex);

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  modules: { auth, error, dark }
});
