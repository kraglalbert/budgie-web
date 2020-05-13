<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-toolbar-title
          ><router-link to="/home">budgie</router-link></q-toolbar-title
        >

        <div style="padding-right: 10px;">
          {{ $store.state.currentUser.name }}
        </div>
        <q-btn flat dense round icon="settings" aria-label="Settings">
          <q-menu>
            <q-list style="min-width: 200px;">
              <q-item clickable v-close-popup @click="showCurrencyPopup = true">
                <q-item-section>
                  <div class="row">
                    Currency:
                    <q-space />
                    <q-badge color="accent">{{ selectedCurrency }}</q-badge>
                  </div>
                </q-item-section>
              </q-item>
              <q-separator />
              <q-item clickable v-close-popup>
                <q-item-section>Settings</q-item-section>
              </q-item>
              <q-separator />
              <q-item clickable v-close-popup @click="logout">
                <q-item-section>Log Out</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
      </q-toolbar>
    </q-header>

    <q-dialog v-model="showCurrencyPopup">
      <CurrencyPopup
        :currency="selectedCurrency"
        @currency-updated="refreshUser"
      />
    </q-dialog>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import CurrencyPopup from "../components/CurrencyPopup";

export default {
  name: "LoggedInLayout",
  components: {
    CurrencyPopup,
  },
  data: function () {
    return {
      selectedCurrency: this.$store.getters.userCurrency,
      showCurrencyPopup: false,
    };
  },
  methods: {
    refreshUser: function () {
      this.showCurrencyPopup = false;
      this.selectedCurrency = this.$store.getters.userCurrency;
    },
    logout: function () {
      this.$store.dispatch("logout").then(this.$router.push({ path: "login" }));
    },
  },
};
</script>

<style lang="scss" scoped>
a {
  color: inherit;
  text-decoration: inherit;
}
</style>
