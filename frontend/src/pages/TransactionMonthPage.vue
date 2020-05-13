<template>
  <BasePage :title="title">
    <q-card flat bordered class="q-mb-md">
      <div v-if="loading" class="text-center">
        <q-spinner color="primary q-ma-md" size="3em" />
      </div>
      <div v-else>
        <q-list class="q-mt-sm q-mb-sm" separator>
          <q-item class="row">
            <q-item-section class="col">
              <q-item-label overline>NET</q-item-label>
              <q-item-label>
                <q-badge
                  v-if="this.totalEarned - this.totalSpent > 0"
                  outline
                  color="positive"
                  >{{ netFormatted }}
                </q-badge>
                <q-badge v-else outline color="negative">{{
                  netFormatted
                }}</q-badge>
              </q-item-label>
            </q-item-section>

            <q-item-section class="col">
              <q-item-label overline>TOTAL EARNED</q-item-label>
              <q-item-label>{{ totalEarnedFormatted }}</q-item-label>
            </q-item-section>

            <q-item-section class="col">
              <q-item-label overline>TOTAL SPENT</q-item-label>
              <q-item-label>{{ totalSpentFormatted }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </div>
    </q-card>
    <q-card flat bordered class="q-mb-md">
      <q-card-section>
        <div class="row q-col-gutter-sm">
          <div class="col">
            <q-select
              outlined
              v-model="transactionType"
              hint="Transaction Type"
              :options="transactionTypeOptions"
              @input="applyFilter"
            />
          </div>
          <div class="col">
            <q-select
              outlined
              v-model="category"
              hint="Category"
              :options="categoryOptions"
              @input="applyFilter"
            />
          </div>
          <div class="col">
            <q-select
              outlined
              v-model="currency"
              hint="Currency"
              :options="currencyOptions"
              @input="applyFilter"
            />
          </div>
          <div class="col">
            <q-select
              outlined
              v-model="displayMode"
              hint="Display Mode"
              :options="displayModeOptions"
              @input="applyFilter"
            />
          </div>
        </div>
      </q-card-section>

      <q-card-section>
        <div v-if="loading" class="text-center">
          <q-spinner color="primary q-ma-md" size="3em" />
        </div>
        <div v-else>
          <TransactionsListItem
            v-for="t in filteredTransactions"
            :key="t.id"
            :transaction="t"
            @refresh="getTransactions"
          />
        </div>
      </q-card-section>
    </q-card>
  </BasePage>
</template>

<script>
import moment from "moment";
import BasePage from "./BasePage.vue";
import TransactionsListItem from "../components/TransactionsListItem.vue";

export default {
  name: "TransactionMonthPage",
  components: {
    BasePage,
    TransactionsListItem,
  },
  data: function () {
    return {
      loading: true,
      transactionTypeOptions: ["All", "Profits", "Spendings"],
      categoryOptions: ["All", "None"],
      currencyOptions: ["All"],
      displayModeOptions: ["Individual", "Grouped"],
      transactionType: "All",
      category: "All",
      currency: "All",
      displayMode: "Individual",
      transactions: [],
      filteredTransactions: [],
      totalSpent: 0,
      totalEarned: 0,
    };
  },
  created: function () {
    this.getCategories();
    this.getTransactions();
  },
  computed: {
    title: function () {
      const month = this.$route.query.month - 1;
      const year = this.$route.query.year;
      // the day doesn't matter
      return moment(new Date(year, month, 1)).utc().format("MMMM YYYY");
    },
    totalSpentFormatted: function () {
      return this.getFormattedDollarAmount(this.totalSpent);
    },
    totalEarnedFormatted: function () {
      return this.getFormattedDollarAmount(this.totalEarned);
    },
    netFormatted: function () {
      const net = this.totalEarned - this.totalSpent;
      return this.getFormattedDollarAmount(net);
    },
  },
  methods: {
    getCategories: function () {
      const userId = this.$store.state.currentUser.id;
      this.$axios
        .get(`/categories/user/${userId}`, {
          headers: {
            Authorization: `Bearer ${this.$store.state.token}`,
          },
        })
        .then((resp) => {
          resp.data.forEach((category) => {
            this.categoryOptions.push(category.name);
          });
        });
    },
    getTransactions: function () {
      this.loading = true;
      const month = this.$route.query.month;
      const year = this.$route.query.year;
      const userId = this.$store.state.currentUser.id;

      this.$axios
        .get(`/transactions/user/${userId}`, {
          params: {
            month: month,
            year: year,
            currency: this.$store.getters.userCurrency,
          },
          headers: {
            Authorization: `Bearer ${this.$store.state.token}`,
          },
        })
        .then((resp) => {
          this.transactions = resp.data.sort(this.compareTransactionDates);

          this.transactions.forEach((transaction) => {
            if (transaction.amount > 0) {
              this.totalEarned += transaction.amount;
            } else {
              this.totalSpent += -1 * transaction.amount;
            }
          });
          // construct filtered list of transactions
          this.applyFilter();
        });
    },
    applyFilter: function () {
      this.loading = true;
      this.filteredTransactions = [];
      this.totalEarned = 0;
      this.totalSpent = 0;

      this.transactions.forEach((transaction) => {
        // TODO: implement the remaining filters
        if (
          this.matchesTypeFilter(transaction) &&
          this.matchesCategoryFilter(transaction)
        ) {
          this.filteredTransactions.push(transaction);
          if (transaction.amount > 0) {
            this.totalEarned += transaction.amount;
          } else {
            this.totalSpent += -1 * transaction.amount;
          }
        }
      });
      this.loading = false;
    },
    matchesTypeFilter: function (transaction) {
      if (
        this.transactionType === "All" ||
        (this.transactionType === "Profits" && transaction.amount > 0) ||
        (this.transactionType === "Spendings" && transaction.amount < 0)
      ) {
        return true;
      } else {
        return false;
      }
    },
    matchesCategoryFilter: function (transaction) {
      if (
        (this.category === "None" && !transaction.category) ||
        this.category === "All" ||
        this.category === transaction.category
      ) {
        return true;
      } else {
        return false;
      }
    },
  },
};
</script>

<style lang="scss" scoped></style>
