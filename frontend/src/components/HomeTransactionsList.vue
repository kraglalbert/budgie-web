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
      @click="showNewTransactionDialog = true"
    />

    <q-dialog v-model="showNewTransactionDialog">
      <HomeNewTransactionPopup @dialog-closed="showNewTransactionDialog=false" />
    </q-dialog>

    <HomeTransactionsListItem
      v-for="t in transactions"
      :key="t.id"
      :transactionName="t.title"
      :transactionSource="t.source"
      :amount="getFormattedDollarAmount(t.amount)"
      :amountNum="t.amount"
      :transactionDate="getFormattedDate(t.date)"
    />
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
  data () {
    return {
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
      return moment(date).utc().format('MMMM Do, YYYY')
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
  margin-bottom: 25px;
  margin-right: 10px;
}
</style>
