<template>
  <BasePage title="Transactions">
    <div v-if="loading" class="text-center">
      <q-spinner color="primary" size="3em" />
    </div>
    <div v-else>
      <TransactionsPageItem
        v-for="transactionMonth in transactionMonths"
        :key="transactionMonth.id"
        :transactionMonth="transactionMonth"
      />
    </div>
  </BasePage>
</template>

<script>
import BasePage from "./BasePage.vue";
import TransactionsPageItem from "../components/TransactionsPageItem.vue";

export default {
  name: "TransactionsPage",
  components: {
    BasePage,
    TransactionsPageItem,
  },
  data: function () {
    return {
      loading: true,
      transactionMonths: [],
    };
  },
  created: function () {
    const userId = this.$store.state.currentUser.id;
    this.$axios
      .get(`/transactions/user/${userId}/months`, {
        headers: {
          Authorization: `Bearer ${this.$store.state.token}`,
        },
        params: {
          currency: this.$store.getters.userCurrency,
        },
      })
      .then((resp) => {
        this.loading = false;
        this.transactionMonths = resp.data.sort(this.compareTransactionDates);
      });
  },
};
</script>

<style lang="scss" scoped></style>
