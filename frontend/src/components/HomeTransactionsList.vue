<template>
  <q-card bordered id="card">
    <q-card-section>
      <div class="text-h6">Transactions This Month</div>
    </q-card-section>

    <q-separator inset />

    <q-btn
      id="new-button"
      color="primary"
      label="Add New"
      @click="showNewTransactionDialog = true"
    />

    <q-dialog v-model="showNewTransactionDialog">
      <HomeNewTransactionPopup
        @transaction-created="getTransactionsForCurrentMonth"
      />
    </q-dialog>

    <div v-if="loading" class="text-center q-ma-md">
      <q-spinner color="primary" size="3em" />
    </div>
    <div v-else-if="transactions.length === 0" class="text-center">
      No transactions to show.
    </div>
    <div v-else>
      <HomeTransactionsListItem
        v-for="t in transactions"
        :key="t.id"
        :transactionName="t.title"
        :transactionSource="t.source"
        :amount="getFormattedDollarAmount(t.amount)"
        :amountNum="t.amount"
        :transactionDate="getFormattedDate(t.date)"
      />
    </div>
  </q-card>
</template>

<script>
import moment from 'moment'
import HomeTransactionsListItem from './HomeTransactionsListItem.vue'
import HomeNewTransactionPopup from './HomeNewTransactionPopup.vue'

export default {
  name: 'HomeTransactionsList',
  components: {
    HomeTransactionsListItem,
    HomeNewTransactionPopup
  },
  data: function () {
    return {
      loading: true,
      transactions: [],
      month: 0,
      year: 0,
      showNewTransactionDialog: false
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
      this.showNewTransactionDialog = false
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
          this.transactions = resp.data.sort(this.compareTransactionDates)
          this.loading = false
        })
    },
    getFormattedDate: function (date) {
      return moment(date)
        .utc()
        .format('MMMM Do, YYYY')
    }
  }
}
</script>

<style lang="scss" scoped>
.space {
  margin-top: 5px;
  margin-bottom: 5px;
}

#new-button {
  margin: 15px;
}

#card {
  width: 100%;
  min-width: 225px;
  margin-top: 25px;
  margin-bottom: 25px;
  margin-right: 10px;
}
</style>
