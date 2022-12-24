<template>
  <a-row
    class="header-content shadow" style="background: white;width: 100%;position: fixed;"
  >
    <div
      class="
      ant-col-xs-0 ant-col-sm-0 ant-col-md-18 ant-col-lg-19 ant-col-xl-19 ant-col-xxl-20
      "
    >
      <a-menu mode="horizontal">
        
      </a-menu>
    </div>

    <div
      class="
      ant-col-xs-24 ant-col-sm-24 ant-col-md-6 ant-col-lg-5 ant-col-xl-5 ant-col-xxl-4 header-left right-tool-bar
      "
    >
      

        <a-menu
          mode="horizontal"
          class="float-right"
        >
          <a-sub-menu>
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
  </a-row>
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
.shadow {
  box-shadow: 0 0.15rem 1.75rem 0 rgb(58 59 69 / 15%);
}
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

.cust-menu .ant-dropdown-menu-item,
.ant-dropdown-menu-submenu-title {
  margin: 5px;
}

.ant-drawer-body {
  padding: 0px;
}
.ant-drawer-body .ant-menu-submenu-title .menu-title {
  color: black;
}
.ant-drawer.ant-drawer-top.ant-drawer-open {
  top: 47px;
  z-index: 10;
}
.ant-drawer.ant-drawer-top {
  z-index: 10;
}
.mobile-menu {
  display: grid;
  grid-template-columns: 33% 33% 33%;
}
.mobile-menu i.ant-menu-submenu-arrow {
  display: none;
}
.mobile-menu .menu-title * {
  display: flex;
  justify-content: center;
}
.mobile-menu:before {
  content: none;
}
.ant-drawer-content-wrapper {
  height: auto !important;
}
.mobile-menu li {
  margin: 10px 0px;
}
.mobile-menu .ant-menu-submenu-title {
  overflow: visible;
}
.mobile-menu .ant-menu-item:last-child {
  margin: auto auto;
}
.mobile-menu .ant-btn.ant-btn-primary {
  padding: 5px;
}
.mobile-menu .fa-plus {
  margin-right: 3px !important;
}
.mobile-menu .ant-menu-item {
  margin-top: 14px;
}
</style>
