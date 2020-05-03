<template>
  <BasePage title="Transactions">
    <TransactionsPageItem
      v-for="transactionMonth in transactionMonths"
      :key="transactionMonth.id"
      :transactionMonth="transactionMonth"
    />
  </BasePage>
</template>

<script>
import BasePage from './BasePage.vue'
import TransactionsPageItem from '../components/TransactionsPageItem.vue'

export default {
  name: 'TransactionsPage',
  components: {
    BasePage,
    TransactionsPageItem
  },
  data: function () {
    return {
      transactionMonths: []
    }
  },
  created: function () {
    const userId = this.$store.state.currentUser.id
    this.$axios
      .get(`/transactions/user/${userId}/months`, {
        headers: {
          Authorization: `Bearer ${this.$store.state.token}`
        }
      })
      .then(resp => {
        this.transactionMonths = resp.data.sort(this.compareTransactionDates)
      })
  }
}
</script>

<style lang="scss" scoped></style>
