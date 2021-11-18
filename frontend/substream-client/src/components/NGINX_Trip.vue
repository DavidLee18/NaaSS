<template>
  <div>
    <section v-if="!onTheTrip">
      <p id="title" class="text-h2 text--primary">NGINX의 놀라움을 생생하게 체험하세요</p>
      <v-container fluid>
        <v-row class="mb-6">
          <v-col v-for="(trip, i) in trips" :key="i" cols="12" md="6" sm="4">
            <v-hover>
              <template v-slot:default="{ hover }">
                <v-card class="mx-auto" max-width="400" outlined 
                  :elevation="hover ? 6 : 0"
                  :to="{ path: '/nginx-trip', query: { type: i + 1 } }">
                  <v-layout justify-center>
                    <v-flex shrink>
                      <v-img width="63" height="73" :src="trip.image"></v-img>
                    </v-flex>
                  </v-layout>
                  <v-card-title>{{ trip.name }}</v-card-title>

                  <!-- <v-card-subtitle class="pb-0">Number 10</v-card-subtitle> -->

                  <v-card-text class="text--primary">
                    <div>{{ trip.description }}</div>
                  </v-card-text>

                  <v-card-actions>
                    <v-btn color="primary" text :to="{ path: '/nginx-trip', query: { type: i + 1 } }"
                      >체험해 보기</v-btn
                    >
                  </v-card-actions>
                </v-card>
              </template>
            </v-hover>
          </v-col>
        </v-row>
      </v-container>
    </section>
    <section v-else>
      <!-- <v-alert v-if="false" :value="tripError" type="warning" transition="scale-transition">
        <v-row align="center">
          <v-col class="grow">
            NGINX 체험관 이용에 문제가 있나요? 다른 체험관을 이용해 보세요
          </v-col>
          <v-col class="shrink">
            <v-btn @click="$router.push('/nginx-trip')">다른 체험관 보기</v-btn>
          </v-col>
        </v-row>
      </v-alert> -->
      <iframe id="portal" :sandbox="sandboxStatement"
      :src="selectedTrip.source" frameBorder="0"
      @error="handleIFrameError($event)" :style="heightStyle"></iframe>
      <!-- <v-dialog
        v-if="false"
        persistent
        max-width="290"
      >
        <v-card>
          <v-card-title class="text-h5">
            죄송합니다
          </v-card-title>
          <v-card-text>
            연결된 체험관에서 오류가 발생했습니다. 
            인터넷 연결을 확인해 주시고 새로고침하거나 다른 체험관을 이용해 주세요. 
          </v-card-text>
          <v-card-actions>
            <v-spacer/>
            <v-btn
              color="green darken-1"
              text
              link to="nginx-trip">
              확인
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog> -->
    </section>
  </div>
</template>

<script>
import axios from "axios";
import { handleError } from '../functions';

export default {
  data: () => ({
    intro: null,
    sandboxRules: ['allow-same-origin', 'allow-scripts', 'allow-forms'],
    suggesting: false,
    tripError: false,
    trips: [
      {
        name: "NGINX Plus",
        description: "작동하고 있는 NGINX의 100개가 넘는 메트릭 정보를 실시간으로 확인하세요",
        image:
          "https://nginxplus.co.kr/wp-content/uploads/2021/08/NGINX-Plus-icon-2020.png",
        source: "https://demo.nginx.com/",
      },
      {
        name: "NGINX Controller",
        description: "API가 제대로 작동하는지 관리하고 Application Delivery 를 손쉽게 관리하세요",
        image:
          "https://nginxplus.co.kr/wp-content/uploads/2021/08/output-onlinepngtools-3.png",
        source: "https://192.168.200.232/login",
      },
      {
        name: "NGINX Instance Manager",
        description:
          "원격으로 NGINX 인스턴스들의 상태를 파악하고, 취약점을 점검하며 손쉽게 패치하세요",
        image:
          "https://nginxplus.co.kr/wp-content/uploads/2021/08/output-onlinepngtools-4.png",
        source: "http://192.168.200.230:11000/",
      },
      {
        name: "NGINX Plus REST API",
        description: "NGINX Plus의 REST API를 살펴보고 직접 호출해 보세요",
        source: "https://demo.nginx.com/swagger-ui/"
      }
    ],
  }),
  computed: {
    heightStyle() {
      const height = this.tripError ? 85 : 95;
      return { height: `${height}vh` };
    },
    loggedIn() { return this.$store.getters.loggedIn },
    onTheTrip() {
      return this.$route.query.type > 0;
    },
    sandboxStatement() { return this.sandboxRules.join(' '); },
    selectedTrip() { return this.trips[this.$route.query.type - 1]; }
  },
  methods: {
    checkIfTripWorks() {
      const tripSource = this.selectedTrip.source;
      axios.get(tripSource).then(res => [res.status === 200, res.statusText])
      .then(([succeeded, statusText]) => {
        console.log(statusText);
        if(!succeeded) { /*this.tripError = true;*/ }
      })
      .catch(error => {
        // this.tripError = true;
        handleError(error);
      });
    },
    handleIFrameError(error) {
      console.log(error);
      console.log('handling error from iframe error event...');
      handleError(error.error);
    }
  },
  watch: {
    loggedIn(val) {
      if(!val) this.$router.push({name: 'Login'});
      else return;
    },
    onTheTrip() {
      if(!this.onTheTrip) this.tripError = false;
      else setTimeout(() => {
        this.tripError = true;
       }, 3000);
    }
  }
};
</script>

<style scoped>
.fab { z-index: 6; }
#title {
  font-size: 6vh;
  margin: 2%;
  text-align: center;
}
iframe {
  width: 100%;
  /* height: 85vh; */
}
section { display: flexbox; }
</style>
