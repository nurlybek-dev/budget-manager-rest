<template>
  <body>
    <header class="header">
      <div class="header__container">
        <div class="header__logo">
          <router-link to="/" class="header__title">BudgetKeeper</router-link>
        </div>
        <div
          class="header__profile dropdown"
          v-if="$store.state.isAuthenticated"
        >
          <div class="profile__email">{{ user.email }}</div>
          <div class="dropdown-content">
            <router-link to="/settings">Настройки</router-link>
            <a href="#" @click="logout">Выйти</a>
          </div>
        </div>
      </div>
    </header>

    <main class="main">
      <div class="main-container">
        <router-view />
      </div>
    </main>

    <footer></footer>
  </body>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      user: {},
    };
  },
  beforeCreate() {
    this.$store.commit("initializeStore");

    if (!this.$store.state.isAuthenticated) {
      this.$router.push("/login");
    }
  },
  mounted() {
    if (this.$store.state.isAuthenticated) {
      axios
        .get("/api/v1/users/me/")
        .then(response => {
          this.user = response.data;
        })
        .catch(error => {
          console.log(error);
        });
    }
  },
  methods: {
    logout() {
      this.$store.commit("removeToken");
      this.$router.push("/login");
    },
  },
};
</script>