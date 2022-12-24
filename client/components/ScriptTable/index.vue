<template>
  <div>
    <a-row class="mb-2" align="middle" justify="start" type="flex">
      <a-col :span="12">
        <a-input-search
          v-model="searchKeyword"
          placeholder="Script info"
          @change="debouncedSearch"
          style="max-width: 250px"
        />
      </a-col>
      <a-col :span="12" class="text-right">
        <a-button
          class="mb-2"
          type="primary"
          ghost
          icon="plus"
          @click="script_popup_visible = true; init_form_state()"
          >Add new Script</a-button
        >
      </a-col>
      
    </a-row>
    <a-table
      ref="table"
      :columns="columns"
      :dataSource="scriptList"
      :pagination="pagination.total > pagination.pageSize ? pagination : false"
      :rowKey="(r, i) => r.id"
      :scroll="{ x: true }"
      :expandedRowKeys="expandedRowKeys"
      bordered
      class="auto-hide-scroll-table"
      @change="handleTableChange"
    >
      <template slot="action" slot-scope="text, record">
        <div class="text-center">
          <a-tooltip
            title="Sửa thông tin Script"
            :arrowPointAtCenter="true"
            :getPopupContainer="(a) => a.parentNode"
          >
            <a-button
              type="primary"
              icon="edit"
              @click="script_popup_visible = true; formState = {...record}"
            ></a-button>
          </a-tooltip>
          <a-tooltip
            title="Hiển thị danh sách Script Actions"
            :arrowPointAtCenter="true"
            :getPopupContainer="(a) => a.parentNode"
          >
            <a-button
              type="primary"
              icon="eye"
              @click="handleViewDetails(record)"
            ></a-button>
          </a-tooltip>
          <a-tooltip
            title="Delete"
            :arrowPointAtCenter="true"
            :getPopupContainer="(a) => a.parentNode"
          >
            <a-button
              type="danger"
              icon="delete"
              @click="handledeleteScript(record)"
            ></a-button>
          </a-tooltip>
        </div>
      </template>

      <template slot="actionTitle"> Action </template>

    </a-table>
    <!-- Popup create Script -->
    <a-modal v-model="script_popup_visible" title="Create new Script" okText="Save"  @ok="handleSaveScript">
      <a-form :model="formState">
        <a-form-item label="Script name">
          <a-input v-model:value="formState.name" />
        </a-form-item>
        <a-form-item label="Game">
          <a-select v-model:value="formState.game" placeholder="Chọn game">
            <a-select-option value="tan_thien_long">Tân Thiên Long</a-select-option>
            <a-select-option value="taoist">Taoist</a-select-option>
            <a-select-option value="tlbb2">Taoist</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="Loop">
          <a-input v-model:value="formState.loop" />
        </a-form-item>
        <a-form-item label="Loop Delay">
          <a-input v-model:value="formState.loop_delay" />
        </a-form-item>
      </a-form>
    </a-modal>

  </div>
</template>

<script>
import { columns} from "./const";
import * as CONST from "@/constants/index.js";
import { mapActions, mapState } from "vuex";
import debounce from "lodash.debounce";
import baseMixin from "@/mixins/baseMixin";
export default {
  name: "ScriptTable",
  mixins: [baseMixin],
  components: { },
  data() {
    return {
      CONST,
      filterUserId: [],
      pagination: {
        pageSize: 100,
        total: 0,
        current: 1,
      },
      searchKeyword: "",
      visible: false,
      expandedRowKeys: [],
      script_popup_visible: false,
      is_add: false,
      formState: {
        "name": "",
        "game": "tan_thien_long",
        "loop": 1,
        "loop_delay": 1000
      }
    };
  },
  computed: {
    ...mapState(["scriptList", "scriptListTotal"]),
    hasExpandedAll() {
      return this.expandedRowKeys.length === this.scriptList.length;
    },
    columns() {
      return columns(this);
    },
    innerColumns() {
      return innerColumns;
    }
  },
  methods: {
    ...mapActions(["fetchScriptList", "deleteScript", "createScript", "updateScript"]),
    async handleTableChange(pagination, filters, sorter) {
      this.pagination = pagination;
      if (!this.pagination.current) {
        this.pagination.current = 1;
      }
      if (!this.pagination.pageSize) {
        this.pagination.pageSize = 10;
      }
      this.filterUserId = filters.created_user ?? [];
      await this.getScriptList();
    },
    handleViewDetails(record) {
      this.$router.push({ path: `script/${record.id}/script-action` });
    },
    init_form_state(){
      this.formState =  {
        "id": null,
        "name": "",
        "game": "tan_thien_long",
        "loop": 1,
        "loop_delay": 1000
      }
    },
    async handleSaveScript(){
      this.script_popup_visible = false
      if (this.formState.id){
        await this.updateScript(this.formState);
      }else {
        await this.createScript(this.formState);
      }
      
      this.getScriptList();

      this.$notification.success({
        message: "Success",
        description: "Cập nhật script thành công",
      });
    },
    async getScriptList() {
      const params = {
        page: this.pagination.current,
        page_size: this.pagination.pageSize,

        created_by: this.filterUserId[0],
        filter: this.searchKeyword,
        orderByDESC: "updated_at",
      };
      await this.fetchScriptList(params);
      this.$set(this.pagination, "total", this.scriptListTotal);
    },

    debouncedSearch: debounce(function (value) {
      this.getScriptList();
    }, 333),

    handledeleteScript(model) {
      this.$confirm({
        title: "Are you sure you want to delete this script?",
        content: "This action cannot be undone.",
        okText: "Yes",
        okType: "danger",
        cancelText: "No",
        centered: true,
        onOk: async () => {
          try {
            await this.deleteScript(model.id);
            this.getScriptList();

            this.$notification.success({
              message: "Success",
              description: "Deleted model successfully",
            });
          } catch (error) {
            this.$notification.error({
              message: "Error",
              description: "Failed to delete model",
            });
          }
        },
      });
    },
  },
  created() {
    this.getScriptList();
  },
};
</script>

<style>
.image-preview {
  width: 64px;
  height: 64px;
}
.small-text {
  font-size: 10px;
  color: #999;
}
.action-btn {
  margin-top: 0.5rem !important;
}
.filter-style {
  width: 100%;
  padding: 4px 0px;
}
.capitalized-text {
  text-transform: capitalize;
}
.info-label {
  font-weight: bold;
  color: #999;
}
.info-value {
  font-weight: bold;
}
</style>