<template>
  <div class="form-container">
    <h1 class="title">Вход</h1>
    <form method="POST" class="form" @submit.prevent="submitForm">
      <ul class="errorlist nonfield" v-if="errors.length">
        <li v-for="error in errors" v-bind:key="error">
          {{ error }}
        </li>
      </ul>
      <div class="form-item">
        <div class="form-item__icon">
          <i class="fas fa-envelope"></i>
        </div>
        <input
          type="email"
          name="username"
          placeholder="Адрес электронной почты"
          maxlength="254"
          required
          id="id_username"
          v-model="email"
        />
      </div>
      <div class="form-item">
        <div class="form-item__icon">
          <i class="fas fa-key"></i>
        </div>
        <input
          type="password"
          name="password"
          autocomplete="current-password"
          placeholder="Пароль"
          required
          id="id_password"
          v-model="password"
        />
      </div>
      <div class="form-actions">
        <button type="submit" class="submit">Войти</button>
      </div>
    </form>
    <div class="form-meta">
      <div>
        <router-link to="/password-reset">Забыли пароль?</router-link>
      </div>
      <div>
        <router-link to="/signup">Регистрация</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "Login",
  data() {
    return {
      email: "",
      password: "",
      errors: [],
    };
  },
  mounted() {
    if(this.$store.state.isAuthenticated) {
      this.$router.push('/');
    }
  },
  methods: {
    async submitForm() {
        this.errors = [];
        if(this.email === '') {
            this.errors.push('E-mail отсуствует')
        }
        if(this.password === '') {
            this.errors.push('Пароль отсуствует')
        }

        if(!this.errors.length) {
            const formData = {
                email: this.email,
                password: this.password
            }

            await axios
                .post('/api/v1/token/login/', formData)
                .then(response => {
                    const token = response.data.auth_token;
                    this.$store.commit('setToken', token);
                    this.$router.go('/');
                })
                .catch(error => {
                    if(error.response) {
                        for(const property in error.response.data) {
                            this.errors.push(`${error.response.data[property]}`);
                        }
                    } else if(error.message) {
                        this.error.push('Что то пошло не так. Пожалуйста попробуйте сново');
                    }
                })
        }
    },
  },
};
</script>