<template>
  <q-card id="container">
    <q-card-section class="row items-center">
      <div class="text-h6">Select Currency</div>
      <q-space />
      <q-btn icon="close" flat round dense v-close-popup />
    </q-card-section>

    <q-card-section>
      <q-form @submit="updateCurrency">
        <q-select
          filled
          class="q-mb-md"
          v-model="selectedCurrency"
          :options="getSupportedCurrencies()"
        >
          <q-tooltip
            anchor="top middle"
            self="bottom middle"
            :offset="[10, 10]"
          >
            Only transactions in this currency will be shown site-wide
          </q-tooltip>
        </q-select>

        <q-btn
          color="primary"
          type="submit"
          label="Update"
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
export default {
  name: "CurrencyPopup",
  props: {
    currency: {
      type: String,
      required: true,
    },
  },
  data: function () {
    return {
      submitting: false,
      selectedCurrency: this.currency,
    };
  },
  methods: {
    updateCurrency: function () {
      this.submitting = true;
      const body = {
        default_currency: this.selectedCurrency,
      };
      const userId = this.$store.state.currentUser.id;

      this.$axios
        .put(`/users/${userId}/settings`, body, {
          headers: {
            Authorization: `Bearer ${this.$store.state.token}`,
          },
        })
        .then((resp) => {
          this.$q.notify({
            color: "green-4",
            position: "top",
            textColor: "white",
            icon: "cloud_done",
            message: "Currency Updated Successfully",
          });
          this.$store.commit("set_user", resp.data);
          this.$emit("currency-updated");
          this.submitting = false;
        })
        .catch((err) => {
          this.$q.notify({
            color: "red-4",
            position: "top",
            textColor: "white",
            icon: "error",
            message: "Something went wrong, please try again",
          });
          this.submitting = false;
        });
    },
  },
};
</script>

<style lang="scss" scoped>
#container {
  width: 30%;
  min-width: 300px;
}
</style>
