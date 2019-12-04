<template>
  <q-page class="flex justify-center">
    <div
      id="container"
      class="row"
    >
      <div class="col-9">
        <HomeTransactionsList />
      </div>
      <div class="col-3">
        <HomeSummaryWidget />
      </div>
    </div>

  </q-page>
</template>

<script>
import HomeTransactionsList from '../components/HomeTransactionsList.vue'
import HomeSummaryWidget from '../components/HomeSummaryWidget.vue'

export default {
  name: 'HomePage',

  components: {
    HomeSummaryWidget,
    HomeTransactionsList
  },
  data () {
    return {

    }
  }
}
</script>

<style lang="scss" scoped>
#container {
  width: 80%;
}
</style>
