import Vue from 'vue'

Vue.mixin({
  methods: {
    getFormattedDollarAmount (amount) {
      let dollarAmount = amount / 100.00
      if (dollarAmount >= 0) {
        return '$' + dollarAmount.toFixed(2)
      } else {
        dollarAmount = dollarAmount * -1
        return '-$' + dollarAmount.toFixed(2)
      }
    }
  }
})
