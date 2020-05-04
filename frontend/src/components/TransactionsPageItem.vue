<template>
  <q-card flat bordered class="q-mb-md">
    <q-card-section>
      <div class="text-h6">{{ transactionMonthDate }}</div>
      <q-list class="q-mt-sm q-mb-sm" bordered separator>
        <q-item class="row">
          <q-item-section class="col">
            <q-item-label overline>NET</q-item-label>
            <q-item-label>
              <q-badge
                v-if="transactionMonth.net > 0"
                outline
                color="positive"
                >{{ net }}</q-badge
              >
              <q-badge v-else outline color="negative">{{ net }}</q-badge>
            </q-item-label>
          </q-item-section>

          <q-item-section class="col">
            <q-item-label overline>TOTAL EARNED</q-item-label>
            <q-item-label>{{ totalEarned }}</q-item-label>
          </q-item-section>

          <q-item-section class="col">
            <q-item-label overline>TOTAL SPENT</q-item-label>
            <q-item-label>{{ totalSpent }}</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>

      <q-btn
        color="primary"
        flat
        label="View Transactions"
        @click="goToTransactionMonthPage"
      />
    </q-card-section>
  </q-card>
</template>

<script>
import moment from "moment";

export default {
  name: "TransactionsPageItem",
  props: {
    transactionMonth: {
      type: Object,
      required: true,
    },
  },
  computed: {
    transactionMonthDate: function () {
      const date = this.transactionMonth.date;
      return moment(date).utc().format("MMMM YYYY");
    },
    totalSpent: function () {
      return this.getFormattedDollarAmount(this.transactionMonth.total_spent);
    },
    totalEarned: function () {
      return this.getFormattedDollarAmount(this.transactionMonth.total_earned);
    },
    net: function () {
      const net =
        this.transactionMonth.total_earned - this.transactionMonth.total_spent;
      return this.getFormattedDollarAmount(net);
    },
  },
  methods: {
    goToTransactionMonthPage: function () {
      const date = new Date(this.transactionMonth.date);
      this.$router.push({
        path: "/transactions",
        query: { month: date.getUTCMonth() + 1, year: date.getFullYear() },
      });
    },
  },
};
</script>

<style lang="scss" scoped></style>
