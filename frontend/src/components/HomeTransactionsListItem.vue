<template>
  <div id="container" class="q-pl-md q-pr-md q-pb-sm q-pt-sm">
    <div class="row">
      <div class="col-9">
        <div class="text-body2 text-weight-medium">{{ transactionName }}</div>
        <div class="text-body2">{{ transactionSource }}</div>
        <div class="text-caption">
          {{ transactionDate }}
        </div>
      </div>
      <div class="col-3">
        <div class="float-right">
          <q-badge
            v-if="amountNum >= 0"
            outline
            color="positive"
            :label="amount"
          />
          <q-badge v-else outline color="negative" :label="amount" />
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
                <q-item clickable v-close-popup>
                  <q-item-section>Edit</q-item-section>
                </q-item>
                <q-separator />
                <q-item clickable v-close-popup>
                  <q-item-section>
                    <div id="remove-button">Remove</div>
                  </q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
        </div>
      </div>
    </div>
  </div>
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
