<template>
  <BasePage title="Manage Categories">
    <q-card>
      <q-card-section class="row items-center">
        <div class="text-subtitle1 text-weight-medium">
          Category Name
        </div>
        <q-space />
        <q-btn
          color="primary"
          label="Add New"
          @click="showCategoryPopup = true"
        />
      </q-card-section>

      <q-separator inset />

      <q-card-section>
        <div v-if="loading" class="text-center q-ma-md">
          <q-spinner color="primary" size="3em" />
        </div>
        <div v-else-if="categories.length == 0" class="text-center q-ma-sm">
          No categories to show.
        </div>
        <div v-else>
          <CategoriesPageItem
            v-for="category in categories"
            :key="category.id"
            :category="category"
            @refresh="getCategories"
          />
        </div>
      </q-card-section>

      <q-dialog v-model="showCategoryPopup">
        <CategoryPopup @category-created="getCategories" />
      </q-dialog>
    </q-card>
  </BasePage>
</template>

<script>
import BasePage from "./BasePage.vue";
import CategoriesPageItem from "../components/CategoriesPageItem.vue";
import CategoryPopup from "../components/CategoryPopup.vue";

export default {
  name: "CategoriesPage",
  components: {
    BasePage,
    CategoriesPageItem,
    CategoryPopup,
  },
  data: function () {
    return {
      categories: [],
      loading: true,
      showCategoryPopup: false,
    };
  },
  created: function () {
    this.getCategories();
  },
  methods: {
    getCategories: function () {
      this.showCategoryPopup = false;
      this.loading = true;

      const userId = this.$store.state.currentUser.id;
      this.$axios
        .get(`/categories/user/${userId}`, {
          headers: {
            "X-CSRF-TOKEN": this.$q.cookies.get("csrf_access_token"),
          },
        })
        .then((resp) => {
          this.loading = false;
          this.categories = resp.data;
        });
    },
  },
};
</script>

<style lang="scss" scoped></style>
