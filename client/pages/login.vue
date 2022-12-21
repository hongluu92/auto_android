<template>
  <a-layout-content class="login-layout">
    <h1 style="text-align: center; font-size: 30px">NERF</h1>
    <div id="components-form-demo-normal-login">
      <a-form :form="form" class="login-form" @submit="handleSubmit">
        <a-form-item>
          <a-input
            v-decorator="[
              'userName',
              {
                rules: [
                  { required: true, message: 'Please enter your username!' },
                ],
              },
            ]"
            placeholder="Username"
          >
            <a-icon
              slot="prefix"
              type="user"
              style="color: rgba(0, 0, 0, 0.25)"
            />
          </a-input>
        </a-form-item>
        <a-form-item>
          <a-input
            v-decorator="[
              'password',
              {
                rules: [
                  { required: true, message: 'Please enter your password!' },
                ],
              },
            ]"
            type="password"
            placeholder="Password"
          >
            <a-icon
              slot="prefix"
              type="lock"
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
            >Log in</a-button
          >
          <div class="text-center">
            <nuxt-link to="/forgot-password">Forgot password?</nuxt-link>
          </div>
        </a-form-item>
        <div v-if="errMessage" class="error-message">{{ errMessage }}</div>
      </a-form>
    </div>
  </a-layout-content>
</template>

<script>
import { mapMutations, mapActions } from "vuex";
import jwt_decode from "jwt-decode";

export default {
  layout: "login",
  middleware: "login",
  beforeCreate() {
    this.form = this.$form.createForm(this, { name: "normal_login" });
  },
  data() {
    return {
      errMessage: "",
      loading: false,
      rootScreen: null,
    };
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      vm.rootScreen = from.name;
    });
  },
  created() {},
  methods: {
    ...mapMutations({
      setCurrentUser: "profile/setCurrentUser",
    }),
    ...mapActions({
      login: "user/login",
    }),
    handleSubmit(e) {
      e.preventDefault();
      this.form.validateFields(async (err, values) => {
        if (!err) this.handleLogin(values);
      });
    },
    async handleLogin(values) {
      this.loading = true;
      let payload = {
        username: values.userName,
        password: values.password,
      };
      try {
        let res = await this.login(payload);
        localStorage.setItem("token", res);
        if (
          this.rootScreen == "index" ||
          !this.rootScreen ||
          this.rootScreen.includes("not-authorized") ||
          this.rootScreen.includes("register") ||
          this.rootScreen.includes("forgot-password") ||
          this.rootScreen.includes("reset-password")
        ) {
          this.$router.push("/");
        } else this.$router.back();
      } catch (error) {
        this.errMessage = error.response.data.error;
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>