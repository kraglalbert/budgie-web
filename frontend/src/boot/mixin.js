import Vue from 'vue'

Vue.mixin({
  methods: {
    getFormattedDollarAmount (amount) {
      const dollarAmount = amount / 100.00
      return '$' + dollarAmount.toFixed(2)
    }
  }
})
