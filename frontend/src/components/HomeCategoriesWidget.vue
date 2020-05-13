<template>
  <q-card bordered id="card" class="q-mt-lg q-ml-sm">
    <q-card-section>
      <div class="text-h6">Categories</div>
    </q-card-section>

    <q-separator inset />

    <q-card-section>
      <div v-if="loading" class="text-center q-ma-md">
        <q-spinner color="primary" size="3em" />
      </div>
      <div v-else>
        <div v-for="category in categories" :key="category.id">
          <q-chip>{{ category.name }}</q-chip>
        </div>

        <div class="row justify-center q-mt-xs">
          <q-btn
            flat
            color="primary"
            label="Manage Categories"
            size="sm"
            @click="goToCategoriesPage"
          />
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  name: "HomeCategoriesWidget",
  data: function () {
    return {
      loading: true,
      categories: [],
    };
  },
  created: function () {
    const userId = this.$store.state.currentUser.id;
    this.$axios
      .get(`/categories/user/${userId}`, {
        headers: {
          Authorization: `Bearer ${this.$store.state.token}`,
        },
      })
      .then((resp) => {
        this.loading = false;
        this.categories = resp.data;
      });
  },
  methods: {
    goToCategoriesPage: function () {
      this.$router.push({ path: "/categories" });
    },
  },
};
</script>

<style lang="scss" scoped>
#card {
  width: 100%;
  min-width: 250px;
}
</style>
