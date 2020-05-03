import Vue from 'vue'

Vue.mixin({
  methods: {
    getFormattedDollarAmount: function (amount) {
      let dollarAmount = amount / 100.0
      if (dollarAmount >= 0) {
        return '$' + dollarAmount.toFixed(2)
      } else {
        dollarAmount = dollarAmount * -1
        return '-$' + dollarAmount.toFixed(2)
      }
    },
    compareTransactionDates: function (t1, t2) {
      if (t1.date < t2.date) return 1
      else return -1
    }
  }
})
