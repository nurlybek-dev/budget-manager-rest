<template>
  <div class="main-page">
    <TransactionForm v-bind:incomes="incomes" v-bind:deposits="deposits" v-bind:expenses="expenses" />
    <div class="dashboard">
      <div class="dashboard__column" style="min-width: 540px">
        <Category v-bind:accounts="incomes" v-bind:category="'income'" v-bind:name="'Доходы'" />
        <Category v-bind:accounts="deposits" v-bind:category="'deposit'" v-bind:name="'Счета'" />
        <Category v-bind:accounts="expenses" v-bind:category="'expense'" v-bind:name="'Затраты'" />
      </div>
      <div class="dashboard__column">
          <Transactions />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Category from '@/components/Category';
import TransactionForm from '@/components/TransactionForm';
import Transactions from '@/components/Transactions';

export default {
  name: "Main",
  components: {
    Category,
    TransactionForm,
    Transactions
  },
  data() {
    return {
      incomes: [],
      deposits: [],
      expenses: [],
    };
  },
  mounted() {
    this.getData();
  },
  methods: {
    async getData() {
      await axios
        .get('/api/v1/accounts/')
        .then(response => {
          response.data.map(account => {
            if(account.type == 1) {
              this.incomes.push(account);
            }
            else if(account.type == 2) {
              this.deposits.push(account);
            }
            else if(account.type == 3) {
              this.expenses.push(account);
            }
          });
        })
        .catch(error => {
          console.log(error);
        });
    },
    accountsTotalActual(accounts) {
      return accounts.reduce((acc, curVal) => {
        return (acc += curVal.actual_amount);
      }, 0);
    },
    accountsTotalPlanned(accounts) {
      return accounts.reduce((acc, curVal) => {
        return (acc += curVal.planned_amount);
      }, 0);
    },
    accountsRemainedPlanned(accounts) {
        let totalActual = this.accountsTotalActual(accounts);
        let totalPlanned = this.accountsTotalPlanned(accounts);
        return Math.max(totalPlanned - totalActual, 0);
    }
  },
  computed: {
    date() {
      const date = new Date();
      return `${this.$store.state.monthNames[date.getMonth()]} ${date.getFullYear()}`;
    },
  },
};
</script>