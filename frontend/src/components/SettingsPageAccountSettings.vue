<template>
  <div class="q-pa-md">
    <!-- Change password section -->
    <div class="text-h6 q-mb-md">Change Password</div>

    <q-form @submit="changePassword" class="q-gutter-sm">
      <q-input
        filled
        dense
        size="xs"
        v-model="oldPassword"
        hint="Old Password"
        type="password"
      />

      <q-input
        filled
        dense
        v-model="newPassword"
        hint="New Password"
        type="password"
      />

      <q-input
        filled
        dense
        v-model="confirmNewPassword"
        hint="Confirm New Password"
        type="password"
        lazy-rules
        :rules="[(val) => val === newPassword || 'Passwords do not match']"
      />

      <q-btn
        label="Update Password"
        type="submit"
        color="primary"
        :disabled="submitting"
      />
    </q-form>
  </div>
</template>

<script>
export default {
  name: "SettingsPageAccountSettings",
  data: function () {
    return {
      submitting: false,
      oldPassword: "",
      newPassword: "",
      confirmNewPassword: "",
    };
  },
  methods: {
    changePassword: function () {
      this.submitting = true;
      const body = {
        old_password: this.oldPassword,
        new_password: this.newPassword,
      };

      this.$axios
        .post("/auth/change-password", body, {
          headers: { "X-CSRF-TOKEN": this.$q.cookies.get("csrf_access_token") },
        })
        .then(() => {
          this.$q.notify({
            color: "green-4",
            position: "top",
            textColor: "white",
            icon: "cloud_done",
            message: "Password Updated Successfully",
          });
          this.submitting = false;
          this.oldPassword = "";
          this.newPassword = "";
          this.confirmNewPassword = "";
        })
        .catch((_err) => {
          console.log(_err);
          this.$q.notify({
            color: "red-4",
            position: "top",
            textColor: "white",
            icon: "error",
            message: "Incorrect Old Password",
          });
          this.submitting = false;
        });
    },
  },
};
</script>

<style lang="scss" scoped></style>
