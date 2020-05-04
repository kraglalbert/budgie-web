<template>
  <q-card bordered id="card">
    <q-card-section>
      <div class="text-h6">Monthly Summary</div>
    </q-card-section>

    <q-separator inset />

    <q-card-section v-if="loading">
      <div class="text-center">
        <q-spinner color="primary" size="3em" />
      </div>
    </q-card-section>

    <q-card-section v-else>
      <div class="space text">
        Spent:
        <span style="float: right;">
          {{ amountSpent }}
        </span>
      </div>
      <div class="space text">
        Earned:
        <span style="float: right;">
          {{ amountEarned }}
        </span>
      </div>
      <div class="space text">
        Remaining Budget:
        <span style="float: right;">
          {{ remainingBudget }}
        </span>
      </div>
      <div class="row justify-center">
        <q-btn
          flat
          color="primary"
          label="View All Months"
          size="sm"
          @click="goToTransactionsPage"
        />
      </div>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  name: "HomeSummaryWidget",
  props: {
    transactions: {
      type: Array,
      required: true,
    },
    loading: {
      type: Boolean,
      required: true,
    },
  },
  data: function () {
    return {};
  },
  computed: {
    amountSpent: function () {
      var spent = 0;
      this.transactions.forEach((t) => {
        if (t.amount < 0) {
          spent += Math.abs(t.amount);
        }
      });
      return this.getFormattedDollarAmount(spent);
    },
    amountEarned: function () {
      var earned = 0;
      this.transactions.forEach((t) => {
        if (t.amount > 0) {
          earned += t.amount;
        }
      });
      return this.getFormattedDollarAmount(earned);
    },
    remainingBudget: function () {
      const user = this.$store.state.currentUser;
      return user.monthly_budget === 0
        ? "N/A"
        : this.getFormattedDollarAmount(user.user_budget - this.amountSpent);
    },
  },
  methods: {
    goToTransactionsPage: function () {
      this.$router.push({ path: "/transactions/all" });
    },
  },
};
</script>

<style lang="scss" scoped>
.space {
  margin-top: 5px;
  margin-bottom: 5px;
}

#card {
  width: 100%;
  min-width: 250px;
  margin-top: 25px;
  margin-left: 10px;
}
</style>
