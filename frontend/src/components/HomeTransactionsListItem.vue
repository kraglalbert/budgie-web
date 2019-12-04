<template>
  <q-card
    flat
    id="container"
  >
    <q-card-section>
      <div class="space text">
        <strong>{{ transactionName }}</strong>
        <span style="float: right;">
          <q-badge
            outline
            color="positive"
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
    amount: String,
    transactionDate: String
  }
}
</script>

<style lang="scss" scoped>
#container:hover {
  background-color: $highlight;
}
</style>
