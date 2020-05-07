<template>
  <div class="row q-pl-md q-mb-sm">
    <div class="col">
      <q-chip>{{ category.name }}</q-chip>
    </div>
    <div class="col">
      <div class="float-right">
        <q-btn flat color="primary" label="Edit" :disabled="submitting" />
        <q-btn
          flat
          color="negative"
          label="Delete"
          :disabled="submitting"
          @click="deleteCategory"
        />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CategoriesPageItem",
  props: {
    category: {
      type: Object,
      required: true,
    },
  },
  data: function () {
    return {
      submitting: false,
    };
  },
  methods: {
    deleteCategory: function () {
      this.submitting = true;

      this.$axios
        .delete(`/categories/${this.category.id}`, {
          headers: {
            Authorization: `Bearer ${this.$store.state.token}`,
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
