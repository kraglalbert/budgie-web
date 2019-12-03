<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-toolbar-title>budgie</q-toolbar-title>

        <div>{{ $store.state.currentUser.name }}</div>
        <q-btn
          flat
          dense
          round
          icon="settings"
          aria-label="Settings"
        >
          <q-menu>
            <q-list style="min-width: 100px">
              <q-item
                clickable
                v-close-popup
              >
                <q-item-section>Settings</q-item-section>
              </q-item>
              <q-separator />
              <q-item
                clickable
                v-close-popup
                @click="logout"
              >
                <q-item-section>Log Out</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
export default {
  name: 'MainLayout',

  data () {
    return {
    }
  },
  methods: {
    logout: function () {
      this.$store.dispatch('logout')
        .then(
          this.$router.push({ path: 'login' })
        )
    }
  }
}
</script>
