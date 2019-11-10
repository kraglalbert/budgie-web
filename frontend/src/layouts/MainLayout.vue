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
        />
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
  }
}
</script>
