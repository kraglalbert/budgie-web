<template>
  <div class="row q-pl-md q-mb-sm">
    <div class="col">
      <q-chip outline>{{ category.name }}</q-chip>
    </div>
    <div class="col">
      <div class="float-right">
        <q-btn
          flat
          color="primary"
          label="Edit"
          :disabled="submitting"
          @click="showCategoryPopup = true"
        />
        <q-btn
          flat
          color="negative"
          label="Delete"
          :disabled="submitting"
          @click="deleteCategory"
        />
      </div>
    </div>

    <q-dialog v-model="showCategoryPopup">
      <CategoryPopup
        :category="category"
        @category-updated="notifyParentToRefresh"
      />
    </q-dialog>
  </div>
</template>

<script>
import CategoryPopup from "./CategoryPopup.vue";

export default {
  name: "CategoriesPageItem",
  components: {
    CategoryPopup,
  },
  props: {
    category: {
      type: Object,
      required: true,
    },
  },
  data: function () {
    return {
      submitting: false,
      showCategoryPopup: false,
    };
  },
  methods: {
    notifyParentToRefresh: function () {
      this.showCategoryPopup = false;
      this.$emit("refresh");
    },
    deleteCategory: function () {
      this.submitting = true;

      this.$axios
        .delete(`/categories/${this.category.id}`, {
          headers: {
            "X-CSRF-TOKEN": this.$q.cookies.get("csrf_access_token"),
          },
        })
        .then((_resp) => {
          this.$q.notify({
            color: "green-4",
            position: "top",
            textColor: "white",
            icon: "cloud_done",
            message: "Category Deleted Successfully",
          });
          this.$emit("refresh");
        });
    },
  },
};
</script>

<style lang="scss" scoped></style>
