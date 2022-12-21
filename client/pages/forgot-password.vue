<template>
  <a-layout-content class="login-layout">
    <h1 style="text-align: center; font-size: 30px">NERF</h1>
    <div id="components-form-demo-normal-login">
      <a-form :form="form" class="login-form" @submit="handleSubmit">
        <a-form-item>
          <a-input
            v-decorator="[
              'email',
              {
                rules: [
                  { required: true, message: 'Please enter your email!' },
                ],
              },
            ]"
            placeholder="Email"
          >
            <a-icon
              slot="prefix"
              type="user"
              style="color: rgba(0, 0, 0, 0.25)"
            />
          </a-input>
        </a-form-item>
        <a-form-item>
          <a-button
            :loading="loading"
            type="primary"
            html-type="submit"
            class="login-form-button"
            >Send instructions</a-button
          >
          <div class="text-center">
            <nuxt-link to="/login">Login</nuxt-link>
          </div>
        </a-form-item>
        <div v-if="errMessage" class="error-message">{{ errMessage }}</div>
      </a-form>
    </div>
  </a-layout-content>
</template>

<script>
import { mapActions } from "vuex";
export default {
  layout: "login",
  beforeCreate() {
    this.form = this.$form.createForm(this, { name: "forgot_password" });
  },
  data() {
    return {
      errMessage: "",
      loading: false,
      rootScreen: null,
    };
  },

  methods: {
    ...mapActions({
      forgotPassword: "user/forgotPassword",
    }),
    handleSubmit(e) {
      e.preventDefault();
      this.form.validateFields(async (err, values) => {
        if (!err) this.handleForgotPassword(values);
      });
    },
    async handleForgotPassword(values) {
      this.loading = true;
      let payload = {
        email: values.email,
      };
      try {
        let res = await this.forgotPassword(payload);
        this.$message.success(res.message);
      } catch (error) {
        this.errMessage = error.response.data.error;
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>