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
      <iframe id="portal" :sandbox="sandboxStatement"
      :src="selectedTrip.source" frameBorder="0"
      @error="handleIFrameError($event)"></iframe>
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
      .then(([succeeded, statusText]) => console.log(statusText, succeeded)).catch(handleError);
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
  height: 95vh;
}
section { display: flexbox; }
</style>
