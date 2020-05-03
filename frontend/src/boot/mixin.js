import Vue from 'vue'
import moment from 'moment'

Vue.mixin({
  methods: {
    getFormattedDate: function (date) {
      return moment(date).format('MMMM Do, YYYY')
    },
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
      var date1 = Date.parse(t1.date)
      var date2 = Date.parse(t2.date)

      if (date1 < date2) return 1
      else return -1
    }
  }
})
