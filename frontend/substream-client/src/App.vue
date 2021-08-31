<template>
  <v-app>
    <v-navigation-drawer
      v-if="loggedIn"
      permanent
      :mini-variant.sync="mini"
      app
    >
      <v-list>
        <v-list-item class="px-2">
          <v-list-item-avatar>
            <v-img
              src="https://randomuser.me/api/portraits/women/85.jpg"
            ></v-img>
          </v-list-item-avatar>
        </v-list-item>

        <v-list-item link>
          <v-list-item-content>
            <v-list-item-title class="text-h6">
              Sandra Adams
            </v-list-item-title>
            <v-list-item-subtitle>sandra_a88@gmail.com</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list nav>
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-folder</v-icon>
          </v-list-item-icon>
          <v-list-item-title>My Files</v-list-item-title>
        </v-list-item>
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-account-multiple</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Shared with me</v-list-item-title>
        </v-list-item>
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-star</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Starred</v-list-item-title>
        </v-list-item>
        <v-btn icon @click.stop="mini = !mini" class="mini-switcher">
          <v-icon>{{ mini ? "mdi-chevron-right" : "mdi-chevron-left" }}</v-icon>
        </v-btn>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar v-if="loggedIn" app color="primary" dark>
      <v-app-bar-nav-icon></v-app-bar-nav-icon>

      <v-toolbar-title>NaaSS</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn icon @click="logout">
        <v-icon> mdi-account-circle </v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data: () => ({
    loggedInDummy: true,
    mini: true,
  }),
  computed: {
    loggedIn() { return this.$store.getters.loggedIn; },
    loggedInReal() { return true && this.loggedIn; }
  },
  methods: {
    logout() { this.$store.dispatch('logout'); this.loggedInDummy = false; }
  }
};
</script>

<style scoped></style>