<template>
  <div class="q-pa-md">
    <div class="text-h6 q-mb-md">Change Primary Currency</div>
    <div class="text-caption q-mb-md">
      Your monthly budget will only apply to your primary currency.
    </div>
    <q-form @submit="updatePrimaryCurrency">
      <q-select
        filled
        dense
        class="q-mb-md"
        v-model="primaryCurrency"
        :options="getSupportedCurrencies()"
      />

      <div class="q-mb-md">
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
      </div>
    </q-form>

    <div class="text-h6 q-mb-md">Change Monthly Budget</div>
    <div class="text-caption q-mb-md">
      This setting allows you to set your monthly budget so that site features
      related to this are enabled.
    </div>

    <q-form @submit="updateBudget">
      <q-input
        filled
        v-model="budget"
        label="Monthly Budget"
        mask="#.##"
        fill-mask="0"
        reverse-fill-mask
        prefix="$"
        lazy-rules
        :rules="[
          (val) =>
            (val !== null && val !== '') || 'Please enter the budget amount',
          (val) => val > 0 || 'Amount cannot be negative or zero',
        ]"
      />

      <q-checkbox
        left-label
        class="q-mb-md"
        v-model="calculateOnNet"
        label="Calculate remaining budget based on net amount?"
      >
        <q-tooltip
          anchor="top middle"
          self="bottom middle"
          :delay="500"
          max-width="300px"
        >
          By default, your remaining budget is calculated based on your
          spendings only. With this setting enabled, your remaining budget will
          be calculated based on the net amount you have lost/gained in a given
          month.
        </q-tooltip>
      </q-checkbox>

      <div>
        <q-btn
          label="Update"
          type="submit"
          color="primary"
          :disabled="submitting"
        />
        <q-spinner
          v-if="submitting"
          color="primary"
          size="2.5em"
          class="q-ml-md"
        />
      </div>
    </q-form>
  </div>
</template>

<script>
export default {
  name: "SettingsPageBudgetSettings",
  data: function () {
    return {
      submitting: false,
      primaryCurrency: "",
      budget: "0.00",
      calculateOnNet: false,
    };
  },
  created: function () {
    const user = this.$store.state.currentUser;

    this.primaryCurrency = user.primary_currency;

    if (user.monthly_budget) {
      this.budget = this.getFormattedDollarAmount(user.monthly_budget).replace(
        /-|\$/g,
        ""
      );
    }
    if (user.monthly_budget_from_net) {
      this.calculateOnNet = user.monthly_budget_from_net;
    }
  },
  methods: {
    updatePrimaryCurrency: function () {
      this.submitting = true;
      const body = {
        primary_currency: this.primaryCurrency,
      };
      const userId = this.$store.state.currentUser.id;

      this.$axios
        .put(`/users/${userId}/settings`, body, {
          headers: {
            "X-CSRF-TOKEN": this.$q.cookies.get("csrf_access_token"),
          },
        })
        .then((resp) => {
          this.$q.notify({
            color: "green-4",
            position: "top",
            textColor: "white",
            icon: "cloud_done",
            message: "Primary Currency Updated Successfully",
          });
          this.$store.commit("set_user", resp.data);
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
    updateBudget: function () {
      this.submitting = true;
      const body = {
        monthly_budget: parseFloat(this.budget) * 100,
        monthly_budget_from_net: this.calculateOnNet,
      };
      const userId = this.$store.state.currentUser.id;

      this.$axios
        .put(`/users/${userId}/settings`, body, {
          headers: {
            "X-CSRF-TOKEN": this.$q.cookies.get("csrf_access_token"),
          },
        })
        .then((resp) => {
          this.$q.notify({
            color: "green-4",
            position: "top",
            textColor: "white",
            icon: "cloud_done",
            message: "Budget Updated Successfully",
          });
          this.$store.commit("set_user", resp.data);
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

<style lang="scss" scoped></style>
