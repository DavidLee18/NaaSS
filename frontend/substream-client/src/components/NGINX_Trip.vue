<template>
  <div>
    <section v-if="!onTheTrip">
      <h1>NGINX의 놀라움을 생생하게 체험하세요</h1>
      <v-container fluid>
        <v-row>
          <v-col v-for="(trip, i) in trips" :key="i" cols="12" sm="4">
            <v-card class="mx-auto" max-width="400">
              <v-img
                class="white--text align-end"
                height="200px"
                :src="trip.image"
              >
                <v-card-title>{{ trip.name }}</v-card-title>
              </v-img>

              <!-- <v-card-subtitle class="pb-0">Number 10</v-card-subtitle> -->

              <v-card-text class="text--primary">
                <div>{{ trip.description }}</div>
              </v-card-text>

              <v-card-actions>
                <v-btn color="primary" text :to="{ path: '/nim-trip', query: { type: i + 1 } }"
                  >체험해 보기</v-btn
                >
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>
    <section v-else-if="onTheTrip">
      <iframe :src="trips[$route.query.type-1].source"></iframe>
      <v-overlay :value="suggesting"></v-overlay>
    </section>
  </div>
</template>

<script>
export default {
  data: () => ({
    selected: 0,
    suggesting: false,
    trips: [
      {
        name: "NGINX Plus",
        description: "작동하고 있는 NGINX의 100개가 넘는 메트릭 정보를 실시간으로 확인하세요",
        image:
          "https://nginxplus.co.kr/wp-content/uploads/2021/08/NGINX-Plus-icon-2020.png",
        source: "https://angular.io",
      },
      {
        name: "NGINX Controller",
        description: "API가 제대로 작동하는지 관리하고 Application Delivery 를 손쉽게 관리하세요",
        image:
          "https://nginxplus.co.kr/wp-content/uploads/2021/08/output-onlinepngtools-3.png",
        source: "https://flutter.dev",
      },
      {
        name: "NGINX Instance Manager",
        description:
          "원격으로 NGINX 인스턴스들의 상태를 파악하고, 취약점을 점검하며 손쉽게 패치하세요",
        image:
          "https://nginxplus.co.kr/wp-content/uploads/2021/08/output-onlinepngtools-4.png",
        source: "https://nate.com",
      },
    ],
  }),
  computed: {
    onTheTrip() {
      return this.$route.query.type > 0;
    }
  }
};
</script>

<style scoped>
.fab { z-index: 6; }
h1 {
  font-size: 6vh;
  text-align: center;
}
iframe {
  width: 100%;
  height: 92vh;
}
section { display: flexbox; }
</style>
