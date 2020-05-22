<template>
  <BasePage>
    <q-card bordered class="q-mt-lg q-mb-md">
      <div class="row">
        <div class="col-3">
          <q-list padding class="rounded-borders">
            <q-item
              clickable
              v-ripple
              :active="selected === 'account'"
              @click="selected = 'account'"
              active-class="my-menu-link"
            >
              <q-item-section avatar>
                <q-icon name="person" />
              </q-item-section>

              <q-item-section>Account</q-item-section>
            </q-item>

            <q-item
              clickable
              v-ripple
              :active="selected === 'budget'"
              @click="selected = 'budget'"
              active-class="my-menu-link"
            >
              <q-item-section avatar>
                <q-icon name="attach_money" />
              </q-item-section>

              <q-item-section>Budget</q-item-section>
            </q-item>
          </q-list>
        </div>

        <q-separator vertical />

        <div class="col">
          <SettingsPageAccountSettings v-if="selected === 'account'" />
          <SettingsPageBudgetSettings v-if="selected === 'budget'" />
        </div>
      </div>
    </q-card>
  </BasePage>
</template>

<script>
import BasePage from "./BasePage.vue";
import SettingsPageAccountSettings from "../components/SettingsPageAccountSettings.vue";
import SettingsPageBudgetSettings from "../components/SettingsPageBudgetSettings.vue";

export default {
  name: "SettingsPage",
  components: {
    BasePage,
    SettingsPageAccountSettings,
    SettingsPageBudgetSettings,
  },
  data: function () {
    return {
      selected: "account",
    };
  },
};
</script>

<style lang="scss" scoped>
.my-menu-link {
  color: $primary;
}
</style>
