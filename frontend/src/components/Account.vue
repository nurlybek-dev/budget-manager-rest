<template>
  <div class="account" :class="[accountClass, { account__hidden: index > 3 && hiddenToggled }]">
    <div class="account__title">
      <router-link :to="account.get_absolute_url">{{
        account.name
      }}</router-link>
    </div>
    <div class="account__icon-wrapper">
      <div
        class="account__fill"
        :style="{ height: account.get_fill_percent + '%' }"
      ></div>
      <router-link :to="account.get_absolute_url">
        <span class="account__icon"><i class="fas fa-wallet"></i></span>
      </router-link>
    </div>
    <div class="account__amount">
      <div class="account__actual-amount">{{ account.current_month_amount }} T</div>
      <div class="account__planned-amount" v-if="account.planned_amount">
        {{ account.planned_amount }} Т
      </div>
    </div>
    <div class="account__edit">
      <i class="fas fa-pencil-alt"></i>
    </div>
    <div class="account__delete">
        <i class="fas fa-trash-alt"></i>
    </div>
  </div>
</template>


<script>
export default {
  name: "Account",
  props: {
    account: Object,
    accountType: String,
    index: Number,
    hiddenToggled: Boolean,
  },
  computed: {
    accountClass() {
      return `account-${this.accountType}`;
    },
  },
};
</script>