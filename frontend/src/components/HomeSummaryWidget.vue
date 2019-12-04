<template>
  <q-card
    bordered
    id="card"
  >
    <q-card-section>
      <div class="text-h6">Monthly Summary</div>
    </q-card-section>

    <q-separator inset />

    <q-card-section>
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
          label="More Info"
          :size="'sm'"
        />
      </div>

    </q-card-section>
  </q-card>
</template>

<script>
export default {
  data () {
    return {
      month: 0,
      year: 0,
      amountSpent: '',
      amountEarned: '',
      remainingBudget: ''
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
        const transactions = resp.data

        var spent = 0
        var earned = 0

        transactions.forEach(t => {
          if (t.amount < 0) {
            spent += Math.abs(t.amount)
          } else {
            earned += t.amount
          }
        })

        const userBudget = user.monthly_budget
        this.amountSpent = this.getFormattedDollarAmount(spent)
        this.amountEarned = this.getFormattedDollarAmount(earned)
        this.remainingBudget = userBudget === 0 ? 'N/A' : this.getFormattedDollarAmount(userBudget - spent)
      })
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

#card {
  width: 100%;
  min-width: 250px;
  margin-top: 25px;
  margin-left: 10px;
}
</style>
