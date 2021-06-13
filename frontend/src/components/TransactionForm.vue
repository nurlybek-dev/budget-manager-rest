<template>
    <div class="add-transaction">
    <form class="add-transaction-form" method="POST" @submit.prevent="submitForm()">
        <label for="account">Из</label>
        <select name="source" id="source" required @change="changeDestinationOptions()" v-model="source">
            <option value='' disabled selected>----------</option>
            <option v-bind:value="account.id" v-for="account in incomes" v-bind:key="account.id">{{ account.name }}</option>
            <option v-bind:value="account.id" v-for="account in deposits" v-bind:key="account.id">{{ account.name }}</option>
        </select>
        <label for="destination">В</label>
        <select name="destination" id="destination" required v-model="destination">
            <option value='' disabled selected>----------</option>
            <option v-bind:value="account.id" v-for="account in deposits" v-bind:key="account.id">{{ account.name }}</option>
            <option v-bind:value="account.id" v-for="account in expenses" v-bind:key="account.id">{{ account.name }}</option>
        </select>
        <label for="amount">Сумму</label>
        <input type="text" name="amount" id="amount" placeholder="1000" required v-model="amount">
        <input type="date" name="date" id="date" required v-model="date">
        <input type="text" name="tags" placeholder="#метка" v-model="tags">
        <input type="text" name="comment" placeholder="комментраии" v-model="comment">
        <button type="submit">+</button>
    </form>
</div>
</template>

<script>
import axios from 'axios';

export default {
  name: "TransactionForm",
  props: {
      incomes: Array,
      deposits: Array,
      expenses: Array,
  },
  data() {
      return {
          source: "",
          destination: "",
          amount: "",
          date: "",
          tags: "",
          comment: "",
      }
  },
  methods: {
      changeDestinationOptions() {
          console.log(this.destination);
      },
      submitForm() {
          const formData = {
              source: this.source,
              destination: this.destination,
              amount: this.amount,
              date: this.date,
              tags: this.tags,
              comment: this.comment,
          };
          axios
            .post('/api/v1/transactions/', formData)
            .then(response => {
                console.log(response);
                this.$store.commit("addTransaction", response.data);
            })
            .catch(error => {
                console.log(error);
            });
      },
  }
};
</script>