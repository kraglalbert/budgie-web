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
</style>
