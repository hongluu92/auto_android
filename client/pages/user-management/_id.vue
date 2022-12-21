<template>
  <div>
    <a-form-model
      class="register-form"
      ref="ruleForm"
      :model="form"
      :rules="rules"
      :label-col="labelCol"
      :wrapper-col="wrapperCol"
    >
      <a-form-model-item ref="name" label="Username" prop="username">
        <a-input class="register-form-item" v-model="form.username" />
      </a-form-model-item>

      <a-form-model-item ref="email" label="Email" prop="email">
        <a-input class="register-form-item" v-model="form.email" />
      </a-form-model-item>

      <a-form-model-item ref="role" label="Role" prop="role">
        <a-select class="register-form-item" v-model="form.role">
          <a-select-option
            :value="role.id"
            v-for="role in roles"
            :key="role.id"
          >
            {{ role.name }}
          </a-select-option>
        </a-select>
      </a-form-model-item>

      <a-form-model-item v-if="id != 'register'" :colon="false">
        <span slot="label"></span>
        <a @click="isPasswordModalVisible = true">Update password</a>
      </a-form-model-item>

      <a-form-model-item
        :wrapper-col="{
          md: { span: 20, offset: 4 },
          xs: { span: 24 },
        }"
      >
        <a-button type="primary" @click="onSubmit" :loading="isLoading">
          {{ id === "register" ? "Create" : "Update" }}
        </a-button>
        <a-button style="margin-left: 10px" @click="resetForm">
          Reset
        </a-button>
      </a-form-model-item>

      <a-modal
        v-model="isPasswordModalVisible"
        :title="`Update password for
    ${form.username}`"
        @ok="onPasswordModalOk"
        @cancel="onPasswordModalCancel"
        :width="450"
      >
        <a-form-model-item
          ref="password"
          label="Password"
          prop="password"
          :labelCol="{
            span: 24,
          }"
          :wrapperCol="{
            span: 24,
          }"
          :colon="false"
        >
          <a-input-password
            class="register-form-item"
            v-model="form.password"
            type="password"
          />
        </a-form-model-item>

        <a-form-model-item
          ref="confirmPassword"
          label="Confirm password"
          prop="confirmPassword"
          :labelCol="{
            span: 24,
          }"
          :wrapperCol="{
            span: 24,
          }"
          :colon="false"
        >
          <a-input-password
            class="register-form-item"
            v-model="form.confirmPassword"
            type="password"
          />
        </a-form-model-item>
      </a-modal>
    </a-form-model>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";
const rules = {
  username: [
    {
      required: true,
      message: "Please input username",
    },
  ],
  email: [
    {
      required: true,
      pattern: new RegExp(
        "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
      ),
      message: "Please input a valid email",
    },
  ],
  role: [
    {
      required: true,
      message: "Please select role",
    },
  ],
  password: [
    {
      required: true,
      message: "Please input password",
    },
  ],
  confirmPassword: [
    {
      required: true,
      message: "Please input confirm password",
    },
  ],
};
export default {
  middleware: "permissions",
  meta: {
    permissions: ["admin"],
  },
  data() {
    return {
      labelCol: { xs: { span: 24 }, md: { span: 4 } },
      wrapperCol: { xs: { span: 24 }, md: { span: 20 } },
      other: "",
      form: {
        username: "",
        email: "",
        role: "",
      },
      rules,
      isLoading: false,
      isPasswordModalVisible: false,
    };
  },
  computed: {
    ...mapState("user", ["roles"]),
    id() {
      return this.$route.params.id;
    },
  },
  methods: {
    ...mapActions("user", [
      "getRoles",
      "register",
      "getUserById",
      "updateUser",
    ]),
    async onSubmit() {
      let isFormValid = await this.$refs.ruleForm.validate();
      if (!isFormValid) return;

      try {
        let payload = {
          username: this.form.username,
          email: this.form.email,
          role: [this.form.role],
          password: this.form.password,
          id: this.id,
        };
        this.isLoading = true;
        if (this.id === "register") {
          await this.register(payload);
        } else {
          await this.updateUser(payload);
        }
        let successMessage =
          this.id === "register"
            ? "User created successfully"
            : "User updated successfully";
        this.$message.success(successMessage);
        this.$router.push("/user-management");
      } catch (error) {
        this.$message.error(error.response.data.message);
      } finally {
        this.isLoading = false;
      }
    },
    resetForm() {
      this.$refs.ruleForm.resetFields();
    },
    onPasswordModalOk() {
      this.isPasswordModalVisible = false;
    },
    onPasswordModalCancel() {
      this.form.password = "";
      this.form.confirmPassword = "";
      this.isPasswordModalVisible = false;
    },
  },
  async created() {
    this.getRoles();
    if (this.id !== "register") {
      let user = await this.getUserById(this.id);
      if (user) {
        this.form.username = user.username;
        this.form.email = user.email;
        this.form.role = user.roleId;
      } else {
        this.$message.error("User not found");
        this.$router.push("/");
      }
    }
  },
};
</script>

<style>
.register-form-item {
  max-width: 400px;
}
.register-form {
  max-width: 600px;
}
</style>