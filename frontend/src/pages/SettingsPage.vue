<template>
  <BasePage>
    <q-card bordered class="q-mt-lg q-mb-md">
      <div class="row">
        <div class="col-3" v-if="$q.screen.width >= 600">
          <q-list padding class="rounded-borders">
            <q-item
              clickable
              v-ripple
              :active="selected === 'Account'"
              @click="selected = 'Account'"
              active-class="menu-item"
            >
              <q-item-section avatar>
                <q-icon name="person" />
              </q-item-section>

              <q-item-section>Account</q-item-section>
            </q-item>

            <q-item
              clickable
              v-ripple
              :active="selected === 'Budget'"
              @click="selected = 'Budget'"
              active-class="menu-item"
            >
              <q-item-section avatar>
                <q-icon name="attach_money" />
              </q-item-section>

              <q-item-section>Budget</q-item-section>
            </q-item>
          </q-list>
        </div>
        <!-- Show dropdown on mobile -->
        <div v-else class="col-12 q-pa-sm">
          <q-select
            filled
            class="q-mb-md"
            v-model="selected"
            :options="options"
          />
        </div>

        <q-separator vertical v-if="$q.screen.width >= 600" />

        <div class="col" v-if="$q.screen.width >= 600">
          <SettingsPageAccountSettings v-if="selected === 'Account'" />
          <SettingsPageBudgetSettings v-if="selected === 'Budget'" />
        </div>
        <div class="col-12" v-else>
          <SettingsPageAccountSettings v-if="selected === 'Account'" />
          <SettingsPageBudgetSettings v-if="selected === 'Budget'" />
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
      selected: "Account",
      options: ["Account", "Budget"],
    };
  },
};
</script>

<style lang="scss" scoped>
.menu-item {
  color: $primary;
}
</style>
