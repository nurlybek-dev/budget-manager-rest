<template>
  <div class="form-container">
    <h1 class="title">Регистрация</h1>
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
      <div class="form-item">
        <div class="form-item__icon">
          <i class="fas fa-key"></i>
        </div>
        <input
          type="password"
          name="password2"
          autocomplete="current-password2"
          placeholder="Повторите пароль"
          required
          id="id_password2"
          v-model="password2"
        />
      </div>
      <div class="form-actions">
        <button type="submit" class="submit">Зарегестрироваться</button>
      </div>
    </form>
    <div class="form-meta">
      <div>
        Уже есть аккаунт?
        <router-link to="/login">Войдите</router-link>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  name: "Signup",
  data() {
      return {
          email: '',
          password: '',
          password2: '',
          errors: [],
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

        if(this.password !== this.password2) {
            this.errors.push('Пароли не совпадают')
        }

        if(!this.errors.length) {
            const formData = {
                email: this.email,
                password: this.password
            }

            await axios
                .post('/api/v1/users/', formData)
                .then(response => {
                    alert("Аккаунт успешно создан, пожалуйста войдите")
                    console.log(response);
                    this.$router.push('/login');
                })
                .catch(error => {
                    if(error.response) {
                        console.log(error.response);
                        for(const property in error.response.data) {
                            this.errors.push(error.response.data[property].join(' '));
                        }
                    } else if(error.message) {
                        this.error.push('Что то пошло не так. Пожалуйста попробуйте сново');
                    }
                })
        }
    },
  }
};
</script>