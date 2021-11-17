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
            <v-img v-if="false"
              src="https://randomuser.me/api/portraits/women/85.jpg"
            ></v-img>
            <v-icon>account_circle</v-icon>
          </v-list-item-avatar>
        </v-list-item>

        <v-list-item v-if="!mini">
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
        <v-list-item link to="nginx-trip">
          <v-list-item-icon>
            <v-icon>accessibility_new</v-icon>
          </v-list-item-icon>
          <v-list-item-title>NGINX 체험관</v-list-item-title>
        </v-list-item>
        <v-btn icon @click.stop="mini = !mini" class="mini-switcher">
          <v-icon>
            {{ mini ? "mdi-chevron-right" : "mdi-chevron-left" }}
          </v-icon>
        </v-btn>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar v-if="loggedIn" :dense="presenting" app color="primary" dark>

      <v-btn v-if="onTheTrip" @click="$router.push('/nginx-trip')" icon>
        <v-icon>arrow_back</v-icon>
      </v-btn>

      <v-toolbar-title @click="$router.push({ name: 'Dashboard' })">
        <button>NaaSS</button>
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <v-progress-circular v-if="loadIFrame" indeterminate></v-progress-circular>

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
      <v-container fluid pa-0>
        <v-alert 
          v-if="$store.getters.errorMessage && false" 
          outlined 
          type="error">
            오류가 발생했습니다: {{$store.getters.errorMessage}}
        </v-alert>
        <div v-if="$store.getters.errorHtml" :v-html="$store.getters.errorHtml"></div>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>

export default {
  data: () => ({
    loadIFrame: false,
    mini: true,
  }),
  computed: {
    dark() { return this.$store.getters.dark },
    loggedIn() { return this.$store.getters.loggedIn },
    onTheTrip() { return this.$route.path === '/nginx-trip' && this.$route.query.type > 0; },
    presenting() {
      if (this.$route.path === '/nginx-trip') {
        // eslint-disable-next-line vue/no-async-in-computed-properties
        setTimeout(() => { this.mini = true; }, 1000);
        return true;
      } else return false;
    }
  },
  methods: {
    logout() { this.$store.dispatch('logout'); },
    toggleTheme() {
      const newDark = !this.$vuetify.theme.dark;
      // this.$vuetify.theme.dark = newDark;
      if(newDark) this.$store.dispatch('preferDark');
      else this.$store.dispatch('preferWhite');
    },
  },
  mounted() {
    this.$store.dispatch('getMyProfile');
    this.$store.dispatch('listenToSystem');
    this.$store.dispatch('listenToPreference');
  },
  watch: {
    dark(val) { console.log(`dark: ${val}`); this.$vuetify.theme.dark = val },
    onTheTrip() {
      if(this.onTheTrip) {
        this.loadIFrame = true;
        setTimeout(() => { this.loadIFrame = false; }, 3000);
      }
      else this.loadIFrame = false;
    }
  }
};
</script>

<style scoped></style>
