<template>
  <v-card elevation="5" class="mx-auto" max-width="400">
    <v-card-title>E-mail 로 로그인하세요</v-card-title>
    <v-form v-model="valid" ref="form">
      <v-card-text>
        <v-text-field
          v-model="email"
          :rules="rules.email"
          label="E-mail *"
          type="email"
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
    email: '',
    trying: false,
    rules: {
      email: [
        (v) => !!v || 'E-mail을 입력해 주세요',
        (v) => /.+@.+/.test(v) || '유효한 E-mail이 아닙니다',
      ],
      password: [(v) => !!v || '비밀번호를 입력해 주세요'],
    },
  }),
  methods: {
    validateAndReport() {
      this.valid = this.$refs.form.validate();
      if (!this.valid) return;
      else {
        this.trying = true;
        this.$store.dispatch('login', {
          email: this.email,
          password: this.password,
        });
        this.trying = false;
        this.$router.push({name: 'Dashboard'});
      }
    },
  },

};
</script>

<style scoped></style>
