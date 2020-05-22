import Vue from "vue";
import moment from "moment";

import Store from "../store";

Vue.mixin({
  methods: {
    getSupportedCurrencies: function () {
      return ["CAD", "USD"];
    },
    getFormattedDate: function (date) {
      return moment(date).utc().format("MMMM Do, YYYY");
    },
    getFormattedDollarAmount: function (amount) {
      let dollarAmount = amount / 100.0;
      if (dollarAmount >= 0) {
        return "$" + dollarAmount.toFixed(2);
      } else {
        dollarAmount = dollarAmount * -1;
        return "-$" + dollarAmount.toFixed(2);
      }
    },
    getRemainingBudget: function (earned, spent) {
      const user = Store.state.currentUser;
      if (!user.monthly_budget) {
        return 0;
      } else {
        if (user.monthly_budget_from_net) {
          const net = spent - earned;
          return user.monthly_budget - net;
        } else {
          return user.monthly_budget - spent;
        }
      }
    },
    compareTransactionDates: function (t1, t2) {
      var date1 = Date.parse(t1.date);
      var date2 = Date.parse(t2.date);

      if (date1 < date2) return 1;
      else return -1;
    },
  },
});
