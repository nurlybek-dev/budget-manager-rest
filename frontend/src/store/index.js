import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    isAuthenticated: false,
    token: '',
    monthNames: [
      "Январь",
      "Фебраль",
      "Март",
      "Апрель",
      "Май",
      "Июнь",
      "Июль",
      "Август",
      "Сентярбь",
      "Октябрь",
      "Ноябрь",
      "Декабрь",
    ],
    weekDays: [
      "Понедельник",
      "Вторниг",
      "Среда",
      "Четверг",
      "Пятница",
      "Суубота",
      "Воскресенье",
    ],
    transactions: [],
    days: [],
  },
  mutations: {
    initializeStore(state) {
      if(localStorage.getItem('token')) {
        state.token = localStorage.getItem('token');
        state.isAuthenticated = true;
        axios.defaults.headers.common['Authorization'] = 'Token ' + state.token;
      } else {
        state.token = '';
        state.mutations = false;
        axios.defaults.headers.common['Authorization'] = '';
      }
    },
    setToken(state, token) {
      state.token = token;
      state.isAuthenticated = true;
      axios.defaults.headers.common['Authorization'] = 'Token ' + token;
      localStorage.setItem('token', token);
    },
    removeToken(state) {
      state.token = '';
      state.isAuthenticated = false;
      axios.defaults.headers.common['Authorization'] = '';
      localStorage.removeItem('token');
    },
    addTransactions(state, transactions) {
      Array.prototype.push.apply(state.transactions, transactions);
      this.commit('regroupTransaction');
    },
    addTransaction(state, transaction) {
      state.transactions.push(transaction);
      this.commit('regroupTransaction');
    },
    removeTransaction(state, transaction) {
      state.transactions = state.transactions.filter(t => {
        return t.id != transaction.id;
      });
      this.commit('regroupTransaction');
    },
    regroupTransaction(state) {
      state.transactions.sort((a, b) => a.date > b.date);
      state.days = state.transactions.reduce((grouped, transaction) => {
        (grouped[transaction["date"]] =
          grouped[transaction["date"]] || []).push(transaction);
        return grouped;
      }, {});
    },
  },
  actions: {
  },
  modules: {
  }
})
