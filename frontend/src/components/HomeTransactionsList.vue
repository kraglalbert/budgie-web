<template>
  <q-card bordered id="card" class="q-mt-lg q-mb-lg q-mr-sm">
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
      <TransactionPopup @transaction-created="notifyParentToRefresh" />
    </q-dialog>

    <div v-if="loading" class="text-center q-ma-md">
      <q-spinner color="primary" size="3em" />
    </div>
    <div v-else-if="transactions.length === 0" class="text-center q-ma-md">
      No transactions to show.
    </div>
    <div v-else>
      <TransactionsListItem
        v-for="t in transactions"
        :key="t.id"
        :transaction="t"
        @refresh="notifyParentToRefresh"
      />
    </div>
  </q-card>
</template>

<script>
import moment from "moment";
import TransactionPopup from "./TransactionPopup.vue";
import TransactionsListItem from "./TransactionsListItem.vue";

export default {
  name: "HomeTransactionsList",
  components: {
    TransactionPopup,
    TransactionsListItem,
  },
  props: {
    transactions: {
      type: Array,
      required: true,
    },
    loading: {
      type: Boolean,
      required: true,
    },
  },
  data: function () {
    return {
      showNewTransactionDialog: false,
    };
  },
  methods: {
    notifyParentToRefresh: function () {
      this.showNewTransactionDialog = false;
      this.$emit("refresh");
    },
  },
};
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
}
</style>
