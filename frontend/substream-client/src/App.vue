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
              안녕하세요
            </v-list-item-title>
            <v-list-item-subtitle>{{$store.getters.email}}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list nav>
        <v-list-item link to="dashboard">
          <v-list-item-icon>
            <v-icon>dashboard</v-icon>
          </v-list-item-icon>
          <v-list-item-title>대시보드</v-list-item-title>
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
        <v-list-item link to="nim-trip">
          <v-list-item-icon>
            <v-icon>settings_applications</v-icon>
          </v-list-item-icon>
          <v-list-item-title>NIM 체험관</v-list-item-title>
        </v-list-item>
        <v-btn icon @click.stop="mini = !mini" class="mini-switcher">
          <v-icon>
            {{ mini ? "mdi-chevron-right" : "mdi-chevron-left" }}
          </v-icon>
        </v-btn>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar v-if="loggedIn" app color="primary" dark>

      <v-toolbar-title>NaaSS</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on" @click="toggleTheme">
            <v-icon>
              {{ $vuetify.theme.dark ? "dark_mode" : "light_mode" }}
            </v-icon>
          </v-btn>
        </template>
        <span>{{ $vuetify.theme.dark ? "어두운 모드. 눌러서 밝은 모드로 전환하세요" : "밝은 모드. 눌러서 어두운 모드로 전환하세요" }}</span>
      </v-tooltip>

      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on" @click="logout">
            <v-icon> logout </v-icon>
          </v-btn>
        </template>
        <span>로그아웃</span>
      </v-tooltip>
      
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <v-alert 
          v-if="$store.getters.errorMessage" 
          outlined 
          type="error">
            오류가 발생했습니다: {{$store.getters.errorMessage}}
        </v-alert>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
/* eslint-disable object-curly-spacing */
/* eslint-disable max-len */

export default {
  data: () => ({
    mini: true,
  }),
  computed: {
    loggedIn() {
      return this.$store.getters.loggedIn;
    },
  },
  methods: {
    logout() {
      this.$store.dispatch('logout');
    },
    toggleTheme() {
      this.$vuetify.theme.dark = !this.$vuetify.theme.dark;
    },
  },
};
</script>

<style scoped></style>
