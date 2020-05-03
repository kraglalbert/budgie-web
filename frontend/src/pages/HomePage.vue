<template>
  <BasePage>
    <div class="row">
      <div class="col-9">
        <HomeTransactionsList
          :transactions="transactions"
          :loading="loading"
          @refresh="getTransactionsForCurrentMonth"
        />
      </div>
      <div class="col-3">
        <HomeSummaryWidget
          :transactions="transactions"
          :loading="loading"
          @refresh="getTransactionsForCurrentMonth"
        />
      </div>
    </div>
  </BasePage>
</template>

<script>
import BasePage from './BasePage.vue'
import HomeTransactionsList from '../components/HomeTransactionsList.vue'
import HomeSummaryWidget from '../components/HomeSummaryWidget.vue'

export default {
  name: 'HomePage',
  components: {
    BasePage,
    HomeSummaryWidget,
    HomeTransactionsList
  },
  data: function () {
    return {
      transactions: [],
      loading: true
    }
  },
  created: function () {
    const currentDate = new Date()
    this.month = currentDate.getMonth()
    this.year = currentDate.getFullYear()

    this.getTransactionsForCurrentMonth()
  },
  methods: {
    getTransactionsForCurrentMonth: function () {
      this.loading = true
      const user = this.$store.state.currentUser
      this.$axios
        .get('/transactions/user/' + user.id, {
          params: {
            month: this.month + 1,
            year: this.year
          },
          headers: {
            Authorization: `Bearer ${this.$store.state.token}`
          }
        })
        .then(resp => {
          this.loading = false
          this.transactions = resp.data.sort(this.compareTransactionDates)
        })
    }
  }
}
</script>

<style lang="scss" scoped></style>
