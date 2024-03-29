<template>
  <v-app>
    <v-navigation-drawer
      v-if="loggedIn"
      permanent
      :mini-variant.sync="mini"
      app
    >
      <v-list>
        <v-tooltip bottom v-if="mini">
          <template v-slot:activator="{ on, attrs }">
            <v-list-item class="px-2" v-bind="attrs" v-on="on">
              <v-list-item-avatar>
                <v-icon>account_circle</v-icon>
              </v-list-item-avatar>
            </v-list-item>
          </template>
          <p>NaaSS 계정</p>
          <p>{{$store.getters.alias}}</p>
          <p>{{$store.getters.email}}</p>
        </v-tooltip>

        <v-list-item class="px-2" v-if="!mini">
          <v-list-item-avatar>
            <v-icon>account_circle</v-icon>
          </v-list-item-avatar>
        </v-list-item>

        <v-list-item v-if="!mini">
          <v-list-item-content>
            <v-list-item-title class="text-h6">
              {{$store.getters.alias}}
            </v-list-item-title>
            <v-list-item-subtitle>{{$store.getters.email}}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <v-list-item v-if="!mini">
          <v-list-item-content>
            <v-dialog v-model="toEditProfile" persistent max-width="600">
              <template v-slot:activator="{ on, attrs }">
                <v-list-item-title v-bind="attrs" v-on="on" @click="readProfile">
                  프로필 수정
                </v-list-item-title>
              </template>

              <v-form v-model="valid" ref="form" @submit="updateProfile">
                <v-card>
                  <v-card-title>
                    프로필 수정
                  </v-card-title>

                  <v-card-text>
                    <v-container>
                      <v-row>
                        <v-col cols="12" sm="6" md="4">
                          <v-text-field 
                            v-model="profile.alias"
                            :rules="rules.alias"
                            label="별칭 *"
                            outlined
                            required/>
                        </v-col>
                        <v-col cols="12" sm="6" md="4">
                          <v-text-field v-model="profile.name" outlined label="이름"/>
                        </v-col>
                        <v-col cols="12" sm="6" md="4">
                          <v-text-field v-model="profile.department" label="소속" outlined/>
                        </v-col>
                        <v-col cols="12" sm="6" md="4">
                          <v-text-field v-model="profile.tel" label="전화번호" type="tel" outlined/>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-card-text>

                  <v-divider></v-divider>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                      color="primary"
                      text
                      :disabled="!valid"
                      @click="updateProfile"
                    >
                      저장
                    </v-btn>
                    <v-btn text @click="toEditProfile = false; resetProfile()">취소</v-btn>
                  </v-card-actions>
                </v-card>
              </v-form>
            </v-dialog>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list nav>
        <v-list-item link to="dashboard">
          <v-list-item-icon>
            <v-icon>dashboard</v-icon>
          </v-list-item-icon>
          <v-list-item-title>NaaSS 소개</v-list-item-title>
        </v-list-item>
        <v-list-item link to="nginx-trip">
          <v-list-item-icon>
            <v-icon>
              subscriptions
            </v-icon>
          </v-list-item-icon>
          <v-list-item-title>NGINX 디지털 체험관</v-list-item-title>
        </v-list-item>
        <v-list-item @click.stop="mini = !mini" class="mini-switcher">
          <v-list-item-icon>
            <v-icon>
              {{ mini ? "arrow_circle_right" : "arrow_circle_left" }}
            </v-icon>
          </v-list-item-icon>
          <v-list-item-title>메뉴 접기</v-list-item-title>
        </v-list-item>
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

      <v-progress-circular v-if="loadIFrame || updatingSubscription" indeterminate></v-progress-circular>

      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on"
            @click="updateSubscription"
            :color="$store.getters.subscribing ? undefined : 'error'"
          >
            <v-icon> {{ $store.getters.subscribing ? 'mark_email_read' : 'unsubscribe' }} </v-icon>
          </v-btn>
        </template>
        <span>{{ $store.getters.subscribing ? 'CVE 구독중' : 'CVE 구독 일시정지됨' }}</span>
      </v-tooltip>

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
          v-if="$store.getters.errorMessage" 
          outlined 
          type="error">
            {{$store.getters.errorMessage}}
        </v-alert>
        <div v-if="$store.getters.errorHtml" :v-html="$store.getters.errorHtml"></div>
        <router-view />
        <v-snackbar v-model="subscriptionUpdated" :color="$vuetify.theme.dark ? 'primary' : undefined">
          {{ $store.getters.subscribing ? '이제 CVE 서비스를 구독합니다' : 'CVE 서비스 구독을 일시정지합니다' }}
        </v-snackbar>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { subscribe, unsubscribe } from './functions';

export default {
  data: () => ({
    loadIFrame: false, //nginx 체험관의 iframe을 로드할 때 true
    mini: true, //navigation drawer가 펼쳐 있는지 여부
    profile: {
      alias: '',
      name: '',
      department: '',
      tel: '',
    },
    rules: {
      alias: [ v => !!v || '별칭을 입력해 주세요' ],
    },
    toEditProfile: false,
    valid: false,
    updatingSubscription: false,
    subscriptionUpdated: false,
  }),
  computed: {
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
    logout() { this.$store.dispatch('logout') },
    readProfile() {
      this.profile.alias = this.$store.getters.alias;
      this.profile.name = this.$store.getters.name;
      this.profile.department = this.$store.getters.department;
      this.profile.tel = this.$store.getters.tel;
    },
    resetProfile() {
      this.profile = {
        alias: '',
        name: '',
        department: '',
        tel: ''
      };
    },
    toggleTheme() {
      const newDark = !this.$vuetify.theme.dark;
      this.$vuetify.theme.dark = newDark;
      if(newDark) this.$store.dispatch('preferDark');
      else this.$store.dispatch('preferWhite');
    },
    updateProfile() {
      this.valid = this.$refs.form.validate();
      if(!this.valid) return;
      else this.$store.dispatch('editProfile', this.profile).finally(() => {
        this.toEditProfile = false;
        this.resetProfile();
      });
    },
    updateSubscription() {
      this.subscriptionUpdated = false;
      this.updatingSubscription = true;
      const finishUpdating = () => {
        this.updatingSubscription = false;
        this.subscriptionUpdated = true;
      };
      if(!this.$store.getters.subscribing) subscribe().finally(finishUpdating);
      else unsubscribe().finally(finishUpdating);
    }
  },
  mounted() {
    this.$store.dispatch('listenToSystem');
    this.$store.dispatch('getMyProfile');
  },
  updated() { this.$vuetify.theme.dark = this.$store.getters.dark },
  watch: {
    onTheTrip() {
      if(this.onTheTrip) {
        this.loadIFrame = true;
        setTimeout(() => { this.loadIFrame = false; }, 3000);
      }
      else this.loadIFrame = false;
    },
  }
};
</script>

<style scoped></style>
