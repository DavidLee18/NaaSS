<template>
  <v-card elevation="5" class="mx-auto" max-width="400">
    <v-layout justify-center align-center>
      <v-flex shrink>
        <p class="text-h5 text--primary">NaaSS 에 오신 것을 환영합니다</p>
      </v-flex>
    </v-layout>
    <v-card-title>사용자 이름으로 로그인하세요</v-card-title>
    <v-form v-model="valid" ref="form">
      <v-card-text>
        <v-text-field
          v-model="username"
          label="사용자 이름(nickname) *"
          :rules="rules.username"
          required
          outlined
        ></v-text-field>
        <v-text-field
          v-model="password"
          :rules="rules.password"
          :append-icon="passwordVisible ? 'mdi-eye' : 'mdi-eye-off'"
          :type="passwordVisible ? 'text' : 'password'"
          label="비밀번호 *"
          required
          outlined
          @click:append="passwordVisible = !passwordVisible"
        ></v-text-field>
      </v-card-text>
      <v-card-actions>
        <v-btn text disabled>비밀번호 재설정</v-btn>
        <v-btn text to="sign-up" color="primary">회원가입하기</v-btn>
        <v-btn
          color="primary"
          :disabled="trying || !valid"
          :loading="trying"
          @click="validateAndReport">로그인</v-btn>
      </v-card-actions>
    </v-form>
  </v-card>
</template>

<script>
export default {
  data: () => ({
    valid: false,
    passwordVisible: false,
    password: '',
    username: '',
    trying: false,
    rules: {
      username: [ v => !!v || '사용자 이름이나 닉네임을 입력해 주세요' ],
      password: [ v => !!v || '비밀번호를 입력해 주세요' ],
    },
  }),
  methods: {
    validateAndReport() {
      this.valid = this.$refs.form.validate();
      if (!this.valid) return;
      else {
        this.trying = true;
        this.$store.dispatch('login', {
          username: this.username,
          password: this.password,
        });
        this.trying = false;
        //this.$router.push({name: 'Dashboard'});
      }
    },
  },

};
</script>

<style scoped>
.text--primary { margin: 2% 0%; }
</style>
