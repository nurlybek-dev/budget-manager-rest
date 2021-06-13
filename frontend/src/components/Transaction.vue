<template>
  <div class="transaction">
    <div class="transaction__view" :class="transactionClass">
      <div class="transaction__body">
        <div class="transaction__categories">
          <div class="transaction__source">
            {{ transaction.source.name }}
          </div>
          <div class="transaction__destination">
            {{ transaction.destination.name }}
          </div>
        </div>
        <div class="transaction__data">
          <div class="transaction__amount">{{ transaction.amount }} Т</div>
          <div class="transaction__tags">{{ transaction.tags }}</div>
          <div class="transaction__comment">
            {{ transaction.comment }}
          </div>
        </div>
      </div>
      <div class="transaction__control">
        <div class="transaction__control-item">
          <i class="fas fa-trash-alt" @click="this.delete()"></i>
        </div>
        <div class="transaction__control-item transaction-form-toggle">
          <i class="fas fa-pencil-alt"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "Transaction",
  props: {
    transaction: Object,
  },
  methods: {
      delete() {
          axios
            .delete(`/api/v1/transactions/${this.transaction.id}/`)
            .then(response => {
                console.log(response);
                this.$store.commit("removeTransaction", this.transaction);
            })
            .catch(error => {
                console.log(error);
            });
      }
  },
  computed: {
    transactionClass() {
      if (this.transaction.source.type == 1 && this.transaction.destination.type == 2) {
        return "transaction_type_positive";
      } else if (
        this.transaction.source.type == 2 &&
        this.transaction.destination.type == 3
      ) {
        return "transaction_type_negative";
      }
      return "";
    },
  },
};
</script>