<template>
  <q-card
    bordered
    id="card"
  >
    <q-card-section>
      <div class="text-h6">Transactions This Month</div>
    </q-card-section>

    <q-separator inset />

    <q-btn
      id="new-button"
      color="primary"
      label="Add New"
    />

    <HomeTransactionsListItem
      v-for="t in transactions"
      :key="t.id"
      :transactionName="t.title"
      :amount="getFormattedDollarAmount(t.amount)"
      :transactionDate="getFormattedDate(t.date)"
    />
  </q-card>
</template>

<script>
import moment from 'moment'
import HomeTransactionsListItem from './HomeTransactionsListItem.vue'

export default {
  name: 'HomeTransactionsList',

  components: {
    HomeTransactionsListItem
  },
  data () {
    return {
      transactions: [],
      month: 0,
      year: 0
    }
  },
  created: function () {
    const currentDate = new Date()
    this.month = currentDate.getMonth()
    this.year = currentDate.getFullYear()

    this.getTransactionsForCurrentMonth()
  },
  methods: {
    getTransactionsForCurrentMonth () {
      const user = this.$store.state.currentUser

      this.$axios.get('/transactions/user/' + user.id, {
        params: {
          month: this.month + 1,
          year: this.year
        },
        headers: {
          'Authorization': this.$store.state.token
        }
      }).then(resp => {
        this.transactions = resp.data
      })
    },
    getFormattedDate (date) {
      return moment((new Date(date))).format('MMMM Do, YYYY')
    }
  }
}
</script>

<style lang="scss" scoped>
h6 {
  margin: 10px;
}

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
  margin-right: 10px;
}
</style>
