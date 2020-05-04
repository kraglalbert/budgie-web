<template>
  <q-card flat bordered class="q-mb-md">
    <q-card-section>
      <div class="text-h6">{{ transactionMonthDate }}</div>
      <q-list class="q-mt-sm q-mb-sm" bordered separator>
        <q-item>
          <q-item-section>
            <q-item-label overline>NET</q-item-label>
            <q-item-label>{{ net }}</q-item-label>
          </q-item-section>
        </q-item>

        <q-item class="row">
          <q-item-section class="col-6">
            <q-item-label overline>TOTAL EARNED</q-item-label>
            <q-item-label>{{ totalEarned }}</q-item-label>
          </q-item-section>
          <q-item-section class="col-6">
            <q-item-label overline>TOTAL SPENT</q-item-label>
            <q-item-label>{{ totalSpent }}</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>

      <q-btn color="primary" flat label="View Transactions" />
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
};
</script>

<style lang="scss" scoped></style>
