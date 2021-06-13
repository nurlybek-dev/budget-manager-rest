<template>
  <div class="feed">
    <div class="day" v-for="(transactions, date) in this.$store.state.days" v-bind:key="date">
      <div class="day__header">
        <span class="day__week-day">{{ weekDay(date) }}</span>
        <span class="day__date">{{ day(date) }}</span>
      </div>
      <div class="day__body">
        <div class="day__transactions">
          <Transaction             
            v-for="transaction in transactions"
            v-bind:key="transaction.id"
            v-bind:transaction="transaction" />
        </div>
      </div>
      <div class="day__footer" :class="footerClass(transactions)">
        <div class="day__balance">
          <div class="day__footer-value"></div>
          <div class="day__footer-title"></div>
        </div>
        <div class="day__total">
          <div class="day__footer-value">{{ dayTotal(transactions) }} T</div>
          <div class="day__footer-title">итого</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Transaction from '@/components/Transaction';

export default {
  name: "Transactions",
  components: {
    Transaction,
  },
  data() {
    return {
      nextPage: 1,
      pageCount: 0,
      limitBottom: 0,
      transactionLoading: false,
    };
  },
  mounted() {
    this.getData();
    window.addEventListener("scroll", this.handleScroll);
  },
  unmounted() {
    window.removeEventListener("scroll", this.handleScroll);
  },
  methods: {
    async getData() {
      this.transactionLoading = true;
      await axios
        .get("/api/v1/transactions/?page=" + this.nextPage)
        .then((response) => {
          this.$store.commit("addTransactions", response.data.results);
          this.pageCount = response.data.count;
          this.nextPage += 1;
          this.limitBottom = window.innerHeight;
        })
        .catch((error) => {
          console.log(error);
        });
      this.transactionLoading = false;
    },
    handleScroll() {
      if (
        this.nextPage <= this.pageCount &&
        document.documentElement.scrollTop >= this.limitBottom &&
        !this.transactionLoading
      ) {
        this.getData();
      }
    },
    footerClass(transactions) {
      let total = this.dayTotal(transactions);
      if (total > 0) {
        return "day__footer-positive";
      } else if (total < 0) {
        return "day__footer-negative";
      } else {
        return "";
      }
    },
    dayTotal(day) {
      return day.reduce((acc, curVal) => {
        if (curVal.destination.type == 3) {
          return (acc -= curVal.amount);
        } else {
          return (acc += curVal.amount);
        }
      }, 0);
    },
    weekDay(date) {
      return this.$store.state.weekDays[new Date(date).getDay()];
    },
    day(date) {
      let d = new Date(date);
      return `${d.getDate()} ${this.$store.state.monthNames[d.getMonth()]}`;
    },
  },
};
</script>