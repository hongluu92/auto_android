<template>
  <div>
    <a-form-model
      class="change-password-form"
      ref="passwordForm"
      :model="form"
      :rules="rules"
      :label-col="labelCol"
      :wrapper-col="wrapperCol"
    >
      <a-form-model-item
        ref="password"
        label="Current password"
        prop="password"
      >
        <a-input-password
          class="change-password-form-item"
          v-model="form.password"
        />
      </a-form-model-item>

      <a-form-model-item
        ref="newPassword"
        label="New password"
        prop="newPassword"
      >
        <a-input-password
          class="change-password-form-item"
          v-model="form.newPassword"
        />
      </a-form-model-item>

      <a-form-model-item
        ref="reEnteredNewPassword"
        label="Confirm password"
        prop="reEnteredNewPassword"
      >
        <a-input-password
          class="change-password-form-item"
          v-model="form.reEnteredNewPassword"
        />
      </a-form-model-item>

      <a-form-model-item
        :wrapper-col="{
          md: { span: 20, offset: 4 },
          xs: { span: 24 },
        }"
      >
        <a-button type="primary" :loading="isLoading" @click="onSubmit">
          Save
        </a-button>
      </a-form-model-item>
    </a-form-model>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";
export default {
  data() {
    return {
      labelCol: { xs: { span: 24 }, md: { span: 4 } },
      wrapperCol: { xs: { span: 24 }, md: { span: 20 } },
      other: "",
      form: {
        password: "",
        newPassword: "",
        reEnteredNewPassword: "",
      },
      rules: {
        password: [
          {
            required: true,
            message: "Please input current password",
          },
        ],
        newPassword: [
          {
            required: true,
            message: "Please input new password",
          },
        ],
        reEnteredNewPassword: [
          {
            required: true,
            validator: (rule, value, callback) => {
              if (!value) {
                callback("Please confirm your password");
              } else if (value !== this.form.newPassword) {
                callback("Passwords do not match!");
              }
              callback();
            },
          },
        ],
      },
      isLoading: false,
    };
  },

  methods: {
    ...mapActions("user", ["changePassword"]),
    async onSubmit() {
      let isFormValid = await this.$refs.passwordForm.validate();
      if (!isFormValid) return;
      try {
        let payload = {
          password: this.form.password,
          newPassword: this.form.newPassword,
        };
        this.isLoading = true;
        await this.changePassword(payload);
        this.$message.success("Password changed successfully");
        this.$router.push("/");
      } catch (error) {
        this.$message.error(error.response.data.message);
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style>
.change-password-form-item {
  max-width: 400px;
}
.change-password-form {
  max-width: 900px;
}
</style>