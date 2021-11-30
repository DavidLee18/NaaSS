
export default {
    state: () => ({
        systemDark: false //시스템 다크 모드 여부
    }),
    mutation: {
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
        async preferDark({ dispatch }) {
            await dispatch('editProfile', { prefer_dark: true }).catch(console.error);
        },
        async preferWhite({ dispatch }) {
            await dispatch('editProfile', { prefer_dark: false }).catch(console.error);
        },
    },
    getters: {
        systemDark: state => state.systemDark,
        dark: (state, getters) => getters.preferDark || state.systemDark
    }
};