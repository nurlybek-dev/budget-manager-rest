<template>
  <div class="category-block dashboard-card">
    <div class="category-block__header">
      <div class="category-block__title">
        <div class="category-block__name">{{ name }}</div>
        <div class="category-block__date">{{ date }}</div>
      </div>
      <div class="category-block__stats">
        <div class="category-block__stats-item">
          <div class="category-block__stats-amount">{{ totalActual }} Т</div>
          <div class="category-block__stats-title">потрачено</div>
        </div>
        <div class="category-block__stats-item">
          <div class="category-block__stats-amount">{{ totalPlanned }} Т</div>
          <div class="category-block__stats-title">бюджет</div>
        </div>
        <div class="category-block__stats-item">
          <div class="category-block__stats-amount">
            {{ remainedPlanned }} Т
          </div>
          <div class="category-block__stats-title">в планах</div>
        </div>
      </div>
    </div>

    <div class="category-block__body">
        <Account
            v-for="(account, index) in accounts" 
            v-bind:key="account.id"
            v-bind:account="account"
            v-bind:accountType="category"
            v-bind:index="index"
            v-bind:hiddenToggled="hiddenToggled" />
      <div
        class="account category_add-account modal-open"
        :class="{ account__hidden: accounts.length > 4 && hiddenToggled }"
        data-target="modal-add-income"
      >
        <div class="account__icon-wrapper">
          <div class="account__icon">
            <i class="fas fa-plus"></i>
          </div>
        </div>
      </div>
    </div>

    <div class="category-block__trigger" 
     :class="{'category-block__trigger-opened': !hiddenToggled}"
     @click="toggle" v-if="accounts.length > 4"></div>
  </div>
</template>


<script>
import Account from '@/components/Account';

export default {
  name: "Category",
  components: {
      Account
  },
  props: {
    name: String,
    category: String,
    accounts: Array,
  },
  data() {
      return {
        hiddenToggled: true
      }
  },
  methods: {
      toggle() {
          this.hiddenToggled = !this.hiddenToggled;
      }
  },
  computed: {
    date() {
      const monthNames = [
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
      ];
      const date = new Date();
      return `${monthNames[date.getMonth()]} ${date.getFullYear()}`;
    },
    totalActual() {
      return this.accounts.reduce((acc, curVal) => {
        return (acc += curVal.current_month_amount);
      }, 0);
    },
    totalPlanned() {
      return this.accounts.reduce((acc, curVal) => {
        return (acc += curVal.planned_amount);
      }, 0);
    },
    remainedPlanned() {
      let totalActual = this.totalActual;
      let totalPlanned = this.totalPlanned;
      return Math.max(totalPlanned - totalActual, 0);
    },
  },
};
</script>