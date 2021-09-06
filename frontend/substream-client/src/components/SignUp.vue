<template>
  <v-card elevation="5" class="mx-auto" max-width="700">
    <v-card-title>환영합니다! E-mail과 비밀번호를 입력하여 구독하세요</v-card-title>
    <v-stepper v-model="progress">
      <v-stepper-header>
        <v-stepper-step :complete="progress > 1" step="1">
          E-mail 입력
        </v-stepper-step>

        <v-divider></v-divider>

        <v-stepper-step :complete="progress > 2" step="2">
          비밀번호 입력
        </v-stepper-step>

        <v-divider></v-divider>

        <v-stepper-step step="3"> 완료 </v-stepper-step>
      </v-stepper-header>

      <v-stepper-items>
        <v-stepper-content step="1">
          <v-card class="mb-12" elevation="0" max-width="400" height="50">
            <v-form v-model="emailValid" ref="email">
              <v-text-field 
                v-model="email" 
                :rules="rules.email" 
                type="email" 
                label="E-mail *" 
                required 
                outlined></v-text-field>
            </v-form>
          </v-card>

          <v-btn color="primary" @click="progress = 2"> 다음 </v-btn>

          <v-btn text @click="$router.go(-1)"> 취소 </v-btn>
        </v-stepper-content>

        <v-stepper-content step="2">
          <v-card class="mb-12" elevation="0" max-width="400" height="50">
            <v-form v-model="passwordValid" ref="password">
              <v-text-field 
                v-model="password" 
                :rules="rules.password" 
                :append-icon="passwordVisible ? 'mdi-eye' : 'mdi-eye-off'" 
                :type="passwordVisible ? 'text' : 'password'" 
                label="비밀번호 *" 
                required
                minlength="6"
                outlined
                @click:append="passwordVisible = !passwordVisible"></v-text-field>
            </v-form>
          </v-card>

          <v-btn 
            color="primary"
            :disabled="trying || !emailValid || !passwordValid"
            :loading="trying"
            @click="validateAndSignUp"> 가입 및 구독하기 </v-btn>

          <v-btn text @click="progress = 1"> 뒤로 가기 </v-btn>
        </v-stepper-content>

        <v-stepper-content step="3">
          <v-card class="mb-12" elevation="0" height="200px">
              <h2>
                  환영합니다! <br> 
                  회원가입과 구독이 완료되었습니다. <br>
                  대시보드로 NaaSS를 둘러보세요
              </h2>
          </v-card>

          <v-btn color="primary" @click="$router.push('login')"> 계속하기 </v-btn>
        </v-stepper-content>
      </v-stepper-items>
    </v-stepper>
  </v-card>
</template>

<script>
export default {
  data: () => ({
    progress: 1,
    emailValid: false,
    passwordValid: false,
    passwordVisible: false,
    password: '',
    email: '',
    trying: false,
    rules: {
      email: [
        (v) => !!v || 'E-mail을 입력해 주세요',
        (v) => /.+@.+/.test(v) || '유효한 E-mail이 아닙니다',
      ],
      password: [
          (v) => !!v || '비밀번호를 입력해 주세요',
          v => v.length >= 6 || '비밀번호는 6자 이상이어야 합니다'
        ],
    },
  }),
  methods: {
    validateAndSignUp() {
      [this.emailValid, this.passwordValid] = [this.$refs.email.validate(), this.$refs.password.validate()];
      if (!this.emailValid || !this.passwordValid) return;
      else {
        this.trying = true;
        this.$store.dispatch('signUp', {
          email: this.email,
          password: this.password,
        });
        this.trying = false;
        this.progress = 3;
      }
    },
  },
};
</script>

<style scoped></style>
