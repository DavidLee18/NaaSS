export default {
    state: () => ({
      errorOccured: false, //에러가 발생했는지 여부
      errorMessage: '', //사용자에게 보여줄 에러 메세지
      errorHtml: '', //서버에서 HTML로 보낸 에러
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