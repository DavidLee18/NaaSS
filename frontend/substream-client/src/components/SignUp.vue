<template>
  <section>
    <v-card elevation="5" class="mx-auto" max-width="700">
      <v-card-title>환영합니다! 기본 정보를 입력하고 구독하세요</v-card-title>
      <v-stepper v-model="progress">
        <v-stepper-header>
          <v-stepper-step :complete="progress > 1" step="1">E-mail 입력</v-stepper-step>

          <v-divider/>

          <v-stepper-step :complete="progress > 2" step="2">사용자 이름 입력</v-stepper-step>

          <v-divider/>

          <v-stepper-step :complete="progress > 3" step="3">비밀번호 입력</v-stepper-step>

          <v-divider/>

          <v-stepper-step :complete="progress > 4" step="4">비밀번호 확인</v-stepper-step>

          <v-divider/>

          <v-stepper-step step="5">완료</v-stepper-step>
        </v-stepper-header>

        <v-stepper-items>
          <v-stepper-content step="1">
            <v-card class="mb-12" elevation="0" max-width="400" height="50">
              <v-form v-model="valid.email" ref="email" @submit="$event.preventDefault()"> <!--바로 submit 처리가 되면 요청이 가지 않고 페이지가 강제 새로고침 됨-->
                <v-text-field 
                  v-model="email" 
                  :rules="rules.email" 
                  type="email" 
                  label="E-mail *" 
                  required 
                  autofocus
                  outlined
                  @keyup.enter="validateAndProceed('email', 2)"></v-text-field>
              </v-form>
            </v-card>
            <v-btn color="primary" @click="validateAndProceed('email', 2)"> 다음 </v-btn>
            <v-btn text @click="$router.go(-1)"> 취소 </v-btn>
          </v-stepper-content>

          <v-stepper-content step="2">
            <v-card class="mb-12" elevation="0" max-width="400" height="50">
              <v-form v-model="valid.username" ref="username" @submit="$event.preventDefault()">
                <v-text-field 
                  v-model="username" 
                  :rules="rules.username"
                  label="사용자 이름(nickname) *" 
                  required 
                  autofocus
                  outlined
                  @keyup.enter="validateAndProceed('username', 3)"></v-text-field>
              </v-form>
            </v-card>
            <v-btn color="primary" @click="validateAndProceed('username', 3)"> 다음 </v-btn>
            <v-btn text @click="progress = 1"> 뒤로 가기 </v-btn>
          </v-stepper-content>

          <v-stepper-content step="3">
            <v-card class="mb-12" elevation="0" max-width="400" height="50">
              <v-form v-model="valid.password" ref="password" @submit="$event.preventDefault()">
                <v-text-field 
                  v-model="password" 
                  :rules="rules.password" 
                  :append-icon="passwordVisible ? 'mdi-eye' : 'mdi-eye-off'" 
                  :type="passwordVisible ? 'text' : 'password'" 
                  label="비밀번호 *" 
                  required
                  minlength="6"
                  autofocus
                  outlined
                  @click:append="passwordVisible = !passwordVisible"
                  @keyup.enter="validateAndProceed('password', 4)"></v-text-field>
              </v-form>
            </v-card>
            <v-btn color="primary" @click="validateAndProceed('password', 4)"> 다음 </v-btn>
            <v-btn text @click="progress = 2"> 뒤로 가기 </v-btn>
          </v-stepper-content>

          <v-stepper-content step="4">
            <v-card class="mb-12" elevation="0" max-width="400" height="50">
              <v-form v-model="valid.passwordAgain" ref="passwordAgain" @submit="$event.preventDefault()">
                <v-text-field 
                  v-model="passwordAgain" 
                  :rules="rules.passwordAgain" 
                  :append-icon="passwordAgainVisible ? 'mdi-eye' : 'mdi-eye-off'" 
                  :type="passwordAgainVisible ? 'text' : 'password'" 
                  label="비밀번호 확인 *" 
                  required
                  autofocus
                  outlined
                  @click:append="passwordAgainVisible = !passwordAgainVisible"
                  @keyup.enter="validateAndSignUp"></v-text-field>
              </v-form>
            </v-card>
            <v-btn 
              color="primary"
              :disabled="trying || !allValid"
              :loading="trying"
              @click="validateAndSignUp"> 가입 및 구독하기 </v-btn>
            <v-btn text @click="progress = 3"> 뒤로 가기 </v-btn>
          </v-stepper-content>

          <v-stepper-content step="5">
            <v-card class="mb-12" elevation="0" height="200px">
                <h2>
                    환영합니다! <br> 
                    회원가입과 구독이 완료되었습니다. <br>
                    대시보드로 NaaSS를 둘러보세요
                </h2>
            </v-card>
            <v-btn color="primary" @click="$router.push('dashboard')"> 계속하기 </v-btn>
          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>
    </v-card>
    <v-dialog v-model="duplicateEmail" persistent max-width="600">
      <v-card>
        <v-card-text>
          이미 등록된 E-mail을 사용할 수 없습니다. <br>
          다른 E-mail로 다시 시도해 주세요.
        </v-card-text>
        <v-card-actions>
          <v-btn @click="resetForms">확인</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </section>
</template>

<script>
export default {
  data: () => ({
    progress: 1,
    passwordVisible: false,
    passwordAgainVisible: false,
    password: '',
    passwordAgain: '',
    email: '',
    username: '',
    trying: false,
    duplicateEmail: false,
    valid: {
      email: false,
      password: false,
      passwordAgain: false,
      username: false,
    }
  }),
  computed: {
    allValid() {
      let v = true;
      for (const name in this.valid) {
        v = v && this.valid[name];
      }
      return v; 
    },
    rules() {
      return {
        email: [  
          v => !!v || 'E-mail을 입력해 주세요',
          v => /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i.test(v) || '유효한 E-mail이 아닙니다',
        ],
        password: [
          v => !!v || '비밀번호를 입력해 주세요',
          v => v.length >= 6 || '비밀번호는 6자 이상이어야 합니다'
        ],
        passwordAgain: [
          v => !!v || '비밀번호를 다시 입력해 주세요',
          v => v === this.password || '비밀번호가 일치하지 않습니다'
        ],
        username: [v => !!v || '사용자 이름(nickname)을 입력해 주세요'],
      };
    }
  },
  methods: {
    resetForms() {
      this.duplicateEmail = false;
      this.email = ''; this.username = ''; this.password = ''; this.passwordAgain = '';
      
      this.progress = 1;
      this.error = false;
    },
    validateAndProceed(name, nextValue) {
      this.valid[name] = this.$refs[name].validate();
      if(this.valid[name]) this.progress = nextValue;
      else return;
    },
    validateAndSignUp() {
      for(const form in this.$refs) { this.valid[form] = this.$refs[form].validate(); }
      if (!this.allValid) return;
      else {
        this.trying = true;
        this.$store.dispatch('createUserAndLogin', { email: this.email, password: this.password }).catch(e => {
          console.error(`error during createUserAndLogin: ${e}`);
          //eror가 undefined로 오지만 서버에서 오는 error는 e-mail이 중복되었을 때 오므로...
          this.duplicateEmail = true;
        }).then(() => {
          this.$store.dispatch('createProfile', { alias: this.username }) }).catch(console.error).finally(() => {
          this.trying = false;
          this.progress = 5;
        });
      }
    },
  },
};
</script>
<style scoped>
v-text-field { margin: 5px; }
</style>