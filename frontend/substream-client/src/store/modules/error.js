export default {
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