<template>
  <section>
    <v-card elevation="5" class="mx-auto" max-width="400">
      <v-layout justify-center align-center>
        <v-flex shrink>
          <p class="text-h5 text--primary">NaaSS 에 오신 것을 환영합니다</p>
        </v-flex>
      </v-layout>
      <v-card-title>E-mail 로 로그인하세요</v-card-title>
      <v-form v-model="valid" ref="form" @submit="validateAndReport">
        <v-card-text>
          <v-text-field
            v-model="email"
            label="E-mail *"
            :rules="rules.email"
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
            @keyup.enter="validateAndReport"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="forgotPassword = true">비밀번호 재설정</v-btn>
          <v-btn text to="sign-up" color="primary">회원가입하기</v-btn>
          <v-btn
            color="primary"
            :disabled="trying || !valid"
            :loading="trying"
            @click="validateAndReport">로그인</v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
    <v-dialog
        v-model="forgotPassword"
        persistent
        max-width="290"
      >
        <v-card>
          <v-card-title class="text-h5">
            비밀번호 재설정 요청
          </v-card-title>
          <v-card-text>
            <p>NaaSS에 가입하신 E-mail을 입력하시면 비밀번호 재설정 메일을 보내드리겠습니다.</p>
            <v-form v-model="emailValid" ref="forgotPasswordForm">
              <v-text-field
                required
                outlined
                v-model="toSendEmail"
                label="E-mail *"
                type="email"
                :rules="rules.email"/>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer/>
            <v-btn color="green darken-1" outlined @click="sendResetEmail">
              확인
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-snackbar v-model="resetEmailSent">비밀번호 재설정 메일을 보냈습니다.</v-snackbar>
  </section>
</template>

<script>
import * as nimrod from '../nimrod';

export default {
  data: () => ({
    forgotPassword: false,
    valid: false,
    emailValid: false,
    passwordVisible: false,
    password: '',
    email: '',
    toSendEmail: '',
    trying: false,
    resetEmailSent: false,
    rules: {
      email: [ 
        v => !!v || 'E-mail을 입력해 주세요',
        v => /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i.test(v) || '올바른 E-mail을 입력해 주세요'
      ],
      password: [ v => !!v || '비밀번호를 입력해 주세요' ],
    },
  }),
  computed: {
    loggedIn() { return this.$store.getters.loggedIn; }
  },
  methods: {
    sendResetEmail() {
      this.emailValid = this.$refs.forgotPasswordForm.validate();
      if(!this.emailValid) return;
      else {
        nimrod.sendPasswordResetEmail(this.toSendEmail).then(sent => {
          this.forgotPassword = false;
          this.resetEmailSent = sent;
        });
      }
    },
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
        //this.$router.push({name: 'Dashboard'});
      }
    }
  },
  watch: {
    loggedIn(val) {
      if(val) this.$router.push({name: 'Dashboard'});
      else return;
    }
  }

};
</script>

<style scoped>
.text--primary { margin: 2% 0%; }
</style>
