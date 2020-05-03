<template>
  <q-card id="container">
    <q-card-section class="row items-center">
      <div class="text-h6">Add New Transaction</div>
      <q-space />
      <q-btn icon="close" flat round dense v-close-popup />
    </q-card-section>

    <q-card-section>
      <q-form @submit="createTransaction">
        <q-input
          filled
          v-model="transactionTitle"
          label="Transaction Title"
          lazy-rules
          :rules="[
            val => (val && val.length > 0) || 'Please enter a transaction title'
          ]"
        />

        <q-input
          filled
          v-model="transactionSource"
          label="Source"
          lazy-rules
          :rules="[val => (val && val.length > 0) || 'Please enter a source']"
        />

        <q-input
          filled
          v-model="transactionAmount"
          label="Amount"
          mask="#.##"
          fill-mask="0"
          reverse-fill-mask
          prefix="$"
          lazy-rules
          :rules="[
            val =>
              (val !== null && val !== '') ||
              'Please enter the transaction amount',
            val => val > 0 || 'Amount cannot be negative or zero'
          ]"
        />

        <q-btn-toggle
          v-model="transactionType"
          class="q-mb-md"
          no-caps
          unelevated
          toggle-color="primary"
          color="white"
          text-color="primary"
          :options="[
            { label: 'Spending', value: 'spending' },
            { label: 'Profit', value: 'profit' }
          ]"
        />

        <q-input filled v-model="transactionDate" mask="date" :rules="['date']">
          <template v-slot:append>
            <q-icon name="event" class="cursor-pointer">
              <q-popup-proxy
                ref="qDateProxy"
                transition-show="scale"
                transition-hide="scale"
              >
                <q-date
                  v-model="transactionDate"
                  @input="() => $refs.qDateProxy.hide()"
                />
              </q-popup-proxy>
            </q-icon>
          </template>
        </q-input>

        <q-btn
          color="primary"
          type="submit"
          label="Add"
          :disabled="submitting"
        />
        <q-spinner
          v-if="submitting"
          color="primary"
          size="2.5em"
          class="q-ml-md"
        />
      </q-form>
    </q-card-section>
  </q-card>
</template>

<script>
import moment from 'moment'

export default {
  name: 'HomeNewTransactionPopup',
  data: function () {
    return {
      submitting: false,
      transactionType: 'spending',
      transactionDate: moment(new Date()).format('YYYY/MM/DD'),
      transactionTitle: '',
      transactionSource: '',
      transactionAmount: ''
    }
  },
  methods: {
    createTransaction: function () {
      this.submitting = true

      const user = this.$store.state.currentUser
      let amount = parseFloat(this.transactionAmount) * 100
      if (this.transactionType === 'spending') {
        amount = -1 * amount
      }

      const date = new Date(this.transactionDate)

      const body = {
        title: this.transactionTitle,
        source: this.transactionSource,
        amount: amount,
        email: user.email,
        year: date.getFullYear(),
        month: date.getUTCMonth() + 1,
        day: date.getUTCDate()
      }

      this.$axios
        .post('/transactions', body, {
          headers: {
            Authorization: `Bearer ${this.$store.state.token}`
          }
        })
        .then(_resp => {
          this.$q.notify({
            color: 'green-4',
            position: 'top',
            textColor: 'white',
            icon: 'cloud_done',
            message: 'Transaction Added Successfully'
          })
          this.submitting = false
          // let parent know to close the dialog
          this.$emit('transaction-created')
        })
        .catch(_err => {
          this.$q.notify({
            color: 'red-4',
            position: 'top',
            textColor: 'white',
            icon: 'error',
            message: 'Something went wrong, please try again'
          })
          this.submitting = false
        })
    }
  }
}
</script>

<style lang="scss" scoped>
#container {
  width: 30%;
  min-width: 300px;
}
</style>
