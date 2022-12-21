<template>
  <a-layout-header
    class="navbar-atv"
    :style="{ position: 'fixed', zIndex: 1000, width: '100%' }"
  >
    <div
      class="
        ant-col-xs-12
        ant-col-sm-12
        ant-col-md-18
        ant-col-lg-19
        ant-col-xl-19
        ant-col-xxl-20
      "
    >
      <a-menu mode="horizontal" :style="{ background: '#0052CC' }">
        <a-menu-item>
          <nuxt-link :to="'/'">
            <a-button class="home-btn" type="primary" icon="home"
              >Home</a-button
            >
          </nuxt-link>
        </a-menu-item>
      </a-menu>
    </div>

    <div
      class="
        ant-col-xs-12
        ant-col-sm-12
        ant-col-md-6
        ant-col-lg-5
        ant-col-xl-5
        ant-col-xxl-4
        header-left
        right-tool-bar
      "
    >
      <div class="text-right">
        <a-dropdown v-if="isAdmin" class="mt-2" :trigger="['click']">
          <a-menu slot="overlay" mode="horizontal">
            <a-menu-item @click="goToUserManagementPage">
              <a-icon type="team" />
              <span>User Management</span>
            </a-menu-item>
          </a-menu>

          <a-tooltip
            title="Admin area"
            :getPopupContainer="(a) => a.parentNode"
          >
            <a-button
              style="margin-left: 8px; bottom: 8px"
              type="primary"
              icon="bank"
              shape="circle"
            />
          </a-tooltip>
        </a-dropdown>

        <a-menu
          mode="horizontal"
          :style="{ background: '#0052CC' }"
          class="float-right"
        >
          <a-sub-menu style="color: white">
            <span slot="title">
              <a-icon type="user" />
              Hello
            </span>

            <a-menu-item @click="goToChangePasswordPage">
              <a-icon type="edit" />
              <span>Change password</span>
            </a-menu-item>

            <a-menu-divider />
            <a-menu-item @click="logout">
              <a-icon type="logout" />
              <span>Log out</span>
            </a-menu-item>
          </a-sub-menu>
        </a-menu>
      </div>
    </div>
  </a-layout-header>
</template>

<script>
import { mapMutations } from "vuex";
import baseMixin from "@/mixins/baseMixin";
export default {
  name: "Nav",
  mixins: [baseMixin],
  methods: {
    ...mapMutations({}),
    logout() {
      localStorage.clear();
      this.$router.push("/login");
    },
    goToChangePasswordPage() {
      this.$router.push("/change-password");
    },
    goToUserManagementPage() {
      this.$router.push("/user-management");
    },
  },
};
</script>

<style>
.ant-menu-item .home-btn .anticon {
  min-width: 14px;
  margin-right: 0px;
  font-size: 14px;
  transition: font-size 0.15s cubic-bezier(0.215, 0.61, 0.355, 1),
    margin 0.3s cubic-bezier(0.645, 0.045, 0.355, 1);
}
@media only screen and (max-width: 768px) {
  .home-btn {
    right: 4px;
  }
}
.cust-menu .ant-dropdown-menu-item,
.ant-dropdown-menu-submenu-title {
  margin: 5px;
}
</style>