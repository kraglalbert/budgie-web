<template>
  <q-layout view="hHh Lpr lff">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          @click="leftDrawerOpen = !leftDrawerOpen"
          icon="menu"
          aria-label="Menu"
        />

        <q-toolbar-title>
          <router-link to="/home">budgie</router-link>
        </q-toolbar-title>

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
              <q-item clickable v-close-popup @click="goToSettingsPage">
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

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      :mini="miniState"
      @mouseover="miniState = false"
      @mouseout="miniState = true"
      bordered
    >
      <q-list>
        <SidebarLink
          title="Transactions"
          caption="View all transactions"
          link="/transactions/all"
          icon="local_atm"
        />
        <SidebarLink
          title="Categories"
          caption="Manage your transaction categories"
          link="/categories"
          icon="category"
        />
        <SidebarLink
          title="Export CSV"
          caption="Export transaction data to CSV"
          link="/home"
          icon="playlist_add_check"
        />
      </q-list>
    </q-drawer>

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
import SidebarLink from "../components/SidebarLink";

export default {
  name: "LoggedInLayout",
  components: {
    CurrencyPopup,
    SidebarLink,
  },
  data: function () {
    return {
      selectedCurrency: this.$store.getters.userCurrency,
      showCurrencyPopup: false,
      leftDrawerOpen: false,
      miniState: true,
    };
  },
  methods: {
    refreshUser: function () {
      this.showCurrencyPopup = false;
      this.selectedCurrency = this.$store.getters.userCurrency;
    },
    goToSettingsPage: function () {
      this.$router.push({ path: "settings" });
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
