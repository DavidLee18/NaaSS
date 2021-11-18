
export default {
    state: () => ({
        preferDark: false,
        systemDark: false
    }),
    mutation: {
        preferDark(state) { state.preferDark = true },
        preferWhite(state) { state.preferDark = false },
        systemDark(state) { state.systemDark = true },
        systemWhite(state) { state.systemDark = false },
    },
    actions: {
        async listenToSystem({ commit }) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
                if(e.matches) commit('systemDark');
                else commit('systemWhite');
            });
        },
        async listenToPreference({ commit, dispatch, getters }) {
            try {
                await dispatch('getMyProfile');
                const preferDark = getters.preferDark;
                if(preferDark) commit('preferDark');
                else commit('preferWhite');
            } catch (error) {
                console.error(error);
                await dispatch('setError', error.message);
            }
        },
        async preferDark({ commit, dispatch }) {
            try {
                await dispatch('editProfile', { prefer_dark: true });
                commit('preferDark');
            } catch (error) {
                console.error(error);
                await dispatch('setError', error.message);
            }
        },
        async preferWhite({ commit, dispatch }) {
            try {
                await dispatch('editProfile', { prefer_dark: false });
                commit('preferWhite');
            } catch (error) {
                console.error(error);
                await dispatch('setError', error.message);
            }
        },
    },
    getters: {
        preferDark: state => state.preferDark,
        systemDark: state => state.systemDark,
        dark: state => state.preferDark || state.systemDark
    }
};