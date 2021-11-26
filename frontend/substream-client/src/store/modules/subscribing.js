export default {
    state: () => ({
        subscribing: false
    }),
    mutation: {
        subscribe(state) { state.subscribing = true },
        unsubscribe(state) { state.subscribing = false }
    },
    actions: {
        async subscribe({ commit, dispatch }) {
            try {
                await dispatch('editProfile', { subscribing: true });
                commit('subscribe');
            } catch (error) { console.error(error) }
        },
        async unsubscribe({ commit, dispatch }) {
            try {
                await dispatch('editProfile', { subscribing: false });
                commit('unsubscribe');
            } catch (error) { console.error(error) }
        },
    },
    getters: {
        subscribing: state => state.subscribing,
    }
};