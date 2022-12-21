<template>
  <div class="user-list">
    <a-row type="flex" justify="space-between" align="middle">
      <a-col :xs="24" :sm="12" class="mb-1">
        <a-input
          v-model="searchKeyword"
          placeholder="Search"
          style="max-width: 250px"
        />
      </a-col>

      <a-col :xs="24" :sm="12" class="user-type-choice mt-1">
        <a-button
          class="mb-2"
          type="primary"
          ghost
          icon="plus"
          @click="handleAddNewUser"
          >Add new user</a-button
        >
        <a-radio-group
          button-style="solid"
          v-model="userType"
          class="mb-2"
          @change="fetchUserList"
        >
          <a-radio-button value="active"> Active Users </a-radio-button>
          <a-radio-button value="deleted"> Inactive Users </a-radio-button>
        </a-radio-group>
      </a-col>
    </a-row>
    <a-table
      :columns="columns"
      :data-source="filteredUsers"
      :pagination="
        users && users.length <= pagination.pageSize ? false : pagination
      "
      :loading="isLoading"
      :row-key="(record) => record.id"
      :bordered="true"
      :scroll="{ x: true }"
      class="auto-hide-scroll-table"
      @change="handleTableChange"
    >
      <template slot="action" slot-scope="text, record">
        <div v-if="userType === 'active'" class="d-inline-flex">
          <a-tooltip title="Edit user">
            <a-button
              type="primary"
              class="mr-1"
              icon="edit"
              @click="handleEdit(record)"
            >
            </a-button>
          </a-tooltip>

          <a-tooltip title="Deactivate user">
            <a-button type="danger" icon="stop" @click="handleDelete(record)">
            </a-button>
          </a-tooltip>
        </div>

        <div v-else-if="userType === 'deleted'" class="d-inline-flex">
          <a-tooltip title="Restore user">
            <a-button
              type="primary"
              icon="undo"
              class="mr-1"
              @click="handleRestore(record)"
            >
            </a-button>
          </a-tooltip>

          <a-tooltip title="Delete user">
            <a-button
              type="danger"
              icon="delete"
              @click="handlePermanentDelete(record)"
            >
            </a-button>
          </a-tooltip>
        </div>
      </template>
    </a-table>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";
import baseMixin from "@/mixins/baseMixin";
export default {
  middleware: "permissions",
  meta: {
    permissions: ["admin"],
  },
  mixins: [baseMixin],
  data() {
    return {
      columns: [
        {
          title: "No.",
          dataIndex: "index",
          key: "index",
          width: 60,
          align: "center",
          customRender: (text, record, index) => {
            return index + 1;
          },
        },
        {
          title: "Username",
          dataIndex: "username",
          key: "username",
        },
        {
          title: "Email",
          dataIndex: "email",
          key: "email",
        },
        {
          title: "Role",
          dataIndex: "permissions",
          key: "role",
          scopedSlots: { customRender: "role" },
        },
        {
          title: "Action",
          key: "action",
          scopedSlots: { customRender: "action" },
          width: 80,
        },
      ],
      pagination: {
        current: 1,
        pageSize: 10,
      },
      isLoading: false,
      userType: "active",
      searchKeyword: "",
    };
  },
  computed: {
    ...mapState("user", ["users"]),
    filteredUsers() {
      if (!this.users) return [];
      return this.users.filter((user) => {
        return (
          user.username
            .toLowerCase()
            .includes(this.searchKeyword.toLowerCase()) ||
          user.email.toLowerCase().includes(this.searchKeyword.toLowerCase()) ||
          user.permissions
            .toLowerCase()
            .includes(this.searchKeyword.toLowerCase())
        );
      });
    },
  },
  methods: {
    ...mapActions("user", [
      "fetchUsers",
      "deleteUser",
      "restoreUser",
      "fetchDeletedUsers",
    ]),
    handleTableChange(pagination) {
      this.pagination = pagination;
      this.fetchUsers({
        page: pagination.current,
        limit: pagination.pageSize,
      });
    },
    handleEdit(record) {
      this.$router.push(`/user-management/${record.id}`);
    },
    handleDelete(record) {
      this.$confirm({
        title: "Are you sure you want to deactivate this user?",
        content: "This action can be undone.",
        okText: "Yes",
        okType: "danger",
        cancelText: "No",
        centered: true,
        onOk: async () => {
          try {
            await this.deleteUser({
              id: record.id,
              isPermanent: false,
            });
            this.fetchUserList();
            this.$message.success("User deactivated successfully");
          } catch (error) {
            this.$message.error("Something went wrong");
          }
        },
      });
    },
    handlePermanentDelete(record) {
      this.$confirm({
        title: "Are you sure you want to permanently delete this user?",
        content: "This action CANNOT be undone.",
        okText: "Yes",
        okType: "danger",
        cancelText: "No",
        centered: true,
        onOk: async () => {
          try {
            await this.deleteUser({
              id: record.id,
              isPermanent: true,
            });
            this.fetchUserList();
            this.$message.success("User deleted successfully");
          } catch (error) {
            this.$message.error("Something went wrong");
          }
        },
      });
    },
    handleRestore(record) {
      this.$confirm({
        title: "Are you sure you want to restore this user?",
        okText: "Yes",
        okType: "primary",
        cancelText: "No",
        centered: true,
        onOk: async () => {
          await this.restoreUser(record.id);
          this.fetchUserList();
        },
      });
    },
    handleAddNewUser() {
      this.$router.push("/user-management/register");
    },
    async fetchUserList() {
      this.isLoading = true;
      if (this.userType === "active") {
        await this.fetchUsers();
      } else {
        await this.fetchDeletedUsers();
      }
      this.isLoading = false;
    },
  },
  async created() {
    this.isLoading = true;
    await this.fetchUserList();
    this.isLoading = false;
  },
};
</script>

<style>
@media screen and (min-width: 768px) {
  .user-type-choice {
    text-align: right;
  }
}
</style>