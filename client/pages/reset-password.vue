<template>
  <a-layout-content class="login-layout">
    <h1 style="text-align: center; font-size: 30px">NERF</h1>
    <div id="components-form-demo-normal-login">
      <a-form :form="form" class="login-form" @submit="handleSubmit">
        <a-form-item>
          <a-input
            v-decorator="[
              'password',
              {
                rules: [
                  {
                    required: true,
                    message: 'Please enter your new password!',
                  },
                ],
              },
            ]"
            placeholder="New password"
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
            >Reset password</a-button
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
    this.form = this.$form.createForm(this, { name: "reset_password" });
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
      resetPassword: "user/resetPassword",
    }),
    handleSubmit(e) {
      e.preventDefault();
      this.form.validateFields(async (err, values) => {
        if (!err) this.handleResetPassword(values);
      });
    },
    async handleResetPassword(values) {
      this.loading = true;
      let payload = {
        password: values.password,
        token: this.$route.query.token,
      };
      try {
        let res = await this.resetPassword(payload);
        this.$message.success(res.message);
        this.$router.push("/login");
      } catch (error) {
        this.errMessage = error.response.data.message;
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>