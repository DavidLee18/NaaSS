<template>
    <section>
        <v-card v-if="!passwordReset" elevation="5" class="mx-auto" max-width="400">
            <!-- <v-layout justify-center align-center>
                <v-flex shrink>
                <p class="text-h5 text--primary">NaaSS 에 오신 것을 환영합니다</p>
                </v-flex>
            </v-layout> -->
            <v-card-title>비밀번호 재설정</v-card-title>
            <v-form v-model="valid" ref="form">
                <v-card-text>
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
                    <v-text-field
                        v-model="passwordAgain"
                        :rules="rules.passwordAgain"
                        :append-icon="passwordAgainVisible ? 'mdi-eye' : 'mdi-eye-off'"
                        :type="passwordAgainVisible ? 'text' : 'password'"
                        label="비밀번호 확인 *"
                        required
                        outlined
                        @click:append="passwordAgainVisible = !passwordAgainVisible"
                        @keyup.enter="resetPassword"
                    ></v-text-field>
                </v-card-text>
                <v-card-actions>
                    <v-btn
                        color="primary"
                        :disabled="trying || !valid"
                        :loading="trying"
                        @click="resetPassword">비밀번호 재설정</v-btn>
                </v-card-actions>
            </v-form>
        </v-card>
        <v-card v-if="passwordReset" class="mb-12">
            <v-card-title>재설정 완료</v-card-title>
            <v-card-text>
                비밀번호 재설정을 완료했습니다 <br>
                바뀐 비밀번호로 로그인 해주세요
            </v-card-text>
            <v-card-actions>
                <v-btn color="primary" @click="$router.push('login')">로그인하기</v-btn>
            </v-card-actions>
        </v-card>
    </section>
</template>

<script>
import * as nimrod from '../nimrod';

export default {
    data: () => ({
        password: '',
        passwordAgain: '',
        passwordVisible: false,
        passwordAgainVisible: false,
        passwordReset: false,
        valid: false,
        trying: false,
    }),
    computed: {
        rules() {
            return {
                password: [
                    v => !!v || '새로운 비밀번호를 입력해 주세요',
                    v => v.length >= 6 || '비밀번호는 6자 이상이어야 합니다'
                ],
                passwordAgain: [
                    v => !!v || '비밀번호를 다시 입력해 주세요',
                    v => v === this.password || '비밀번호가 일치하지 않습니다'
                ],
            };
        }
    },
    methods: {
        resetPassword() {
            this.valid = this.$refs.form.validate();
            if(!this.valid) return;
            else {
                this.trying = true;
                const token = this.$route.query.token;
                nimrod.resetPassword(token, this.password).then(reset => {
                    this.passwordReset = reset;
                }).finally(() => { this.trying = false });
            }
        }
    }
}
</script>

<style scoped></style>