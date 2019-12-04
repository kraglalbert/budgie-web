<template>
  <q-card
    flat
    id="container"
  >
    <q-card-section>
      <div class="space text">
        <strong>{{ transactionName }}</strong> - {{ transactionSource }}
        <span style="float: right;">
          <q-badge
            v-if="amountNum >= 0"
            outline
            color="positive"
            :label="amount"
          />
          <q-badge
            v-else
            outline
            color="negative"
            :label="amount"
          />
          <q-btn
            flat
            dense
            round
            icon="more_vert"
            aria-label="Edit"
            style="margin-left: 5px"
          >
            <q-menu>
              <q-list style="min-width: 100px">
                <q-item
                  clickable
                  v-close-popup
                >
                  <q-item-section>Edit</q-item-section>
                </q-item>
                <q-separator />
                <q-item
                  clickable
                  v-close-popup
                >
                  <q-item-section>
                    <div id="remove-button">Remove</div>
                  </q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
        </span>
      </div>
      <div class="space text">
        {{ transactionDate }}
      </div>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  name: 'HomeTransactionsListItem',

  props: {
    transactionName: String,
    transactionSource: String,
    amount: String,
    amountNum: Number,
    transactionDate: String
  }
}
</script>

<style lang="scss" scoped>
#container:hover {
  background-color: $highlight;
}

#remove-button {
  color: $negative;
}
</style>
