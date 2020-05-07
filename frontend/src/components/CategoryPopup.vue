<template>
  <q-card id="container">
    <q-card-section class="row items-center">
      <div class="text-h6">{{ title }}</div>
      <q-space />
      <q-btn icon="close" flat round dense v-close-popup />
    </q-card-section>

    <q-card-section>
      <q-form @submit="onSubmit">
        <q-input
          filled
          v-model="categoryName"
          label="Category Name"
          lazy-rules
          :rules="[
            (val) => (val && val.length > 0) || 'Please enter a category name',
          ]"
        />

        <q-btn
          color="primary"
          type="submit"
          :label="buttonLabel"
          :disabled="submitting"
        />
        <q-spinner
          v-if="submitting"
          color="primary"
          size="2.5em"
          class="q-ml-md"
        />
      </q-form>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  name: "CategoryPopup",
  props: {
    category: Object,
  },
  data: function () {
    return {
      submitting: false,
      title: "Add Category",
      buttonLabel: "Add",
      categoryName: "",
    };
  },
  created: function () {
    if (this.category) {
      this.title = "Edit Category";
      this.buttonLabel = "Update";

      this.categoryName = this.category.name;
    }
  },
  methods: {
    onSubmit: function () {
      if (this.category) {
        this.updateCategory();
      } else {
        this.createCategory();
      }
    },
    createCategory: function () {
      this.submitting = true;

      const body = {
        user_id: this.$store.state.currentUser.id,
        name: this.categoryName,
      };

      this.$axios
        .post("/categories", body, {
          headers: {
            Authorization: `Bearer ${this.$store.state.token}`,
          },
        })
        .then((resp) => {
          this.$q.notify({
            color: "green-4",
            position: "top",
            textColor: "white",
            icon: "cloud_done",
            message: "Category Added Successfully",
          });
          this.submitting = false;
          this.$emit("category-created");
        })
        .catch(() => {
          this.$q.notify({
            color: "red-4",
            position: "top",
            textColor: "white",
            icon: "error",
            message: "Something went wrong, please try again",
          });
          this.submitting = false;
        });
    },
    updateCategory: function () {},
  },
};
</script>

<style lang="scss" scoped>
#container {
  width: 30%;
  min-width: 300px;
}
</style>
