<template>
  <div id="container" class="q-pl-md q-pr-md q-pb-sm q-pt-sm">
    <div class="row">
      <div class="col-9">
        <div class="text-body2 text-weight-medium">{{ transaction.title }}</div>
        <div class="text-body2">{{ transaction.source }}</div>
        <div class="text-caption">
          {{ getFormattedDate(transaction.date) }}
        </div>
      </div>

      <div class="col-3">
        <div class="float-right">
          <q-badge
            v-if="transaction.amount >= 0"
            outline
            color="positive"
            :label="getFormattedDollarAmount(transaction.amount)"
          />
          <q-badge
            v-else
            outline
            color="negative"
            :label="getFormattedDollarAmount(transaction.amount)"
          />
          <q-btn
            flat
            dense
            round
            icon="more_vert"
            aria-label="Edit"
            style="margin-left: 5px;"
          >
            <q-menu>
              <q-list style="min-width: 100px;">
                <q-item
                  clickable
                  v-close-popup
                  @click="showTransactionPopup = true"
                >
                  <q-item-section>Edit</q-item-section>
                </q-item>
                <q-separator />
                <q-item clickable v-close-popup @click="deleteTransaction">
                  <q-item-section>
                    <div id="remove-button">Remove</div>
                  </q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
        </div>
      </div>

      <q-dialog v-model="showTransactionPopup">
        <TransactionPopup
          :transaction="transaction"
          @transaction-updated="notifyParentToRefresh"
        />
      </q-dialog>
    </div>
  </div>
</template>

<script>
import TransactionPopup from "./TransactionPopup.vue";

export default {
  name: "TransactionsListItem",
  components: {
    TransactionPopup,
  },
  props: {
    transaction: {
      type: Object,
      required: true,
    },
  },
  data: function () {
    return {
      showTransactionPopup: false,
    };
  },
  methods: {
    notifyParentToRefresh: function () {
      this.showTransactionPopup = false;
      this.$emit("refresh");
    },
    deleteTransaction: function () {
      this.$axios
        .delete(`/transactions/${this.transaction.id}`, {
          headers: {
            Authorization: `Bearer ${this.$store.state.token}`,
          },
        })
        .then((_resp) => {
          this.$q.notify({
            color: "green-4",
            position: "top",
            textColor: "white",
            icon: "cloud_done",
            message: "Transaction Deleted Successfully",
          });
          this.$emit("refresh");
        })
        .catch((_err) => {
          this.$q.notify({
            color: "red-4",
            position: "top",
            textColor: "white",
            icon: "error",
            message: "Something went wrong, please try again",
          });
        });
    },
  },
};
</script>

<style lang="scss" scoped>
#container:hover {
  background-color: $highlight;
}

#remove-button {
  color: $negative;
}
</style>
