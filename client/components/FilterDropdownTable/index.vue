<template>
  <div class="ant-table-filter-dropdown ant-dropdown-content">
    <a-radio-group
      v-model="value"
      class="filter-style filter-credit-status"
      @change="(e) => handleChangeCheckbox(e)"
    >
      <a-radio
        v-for="filter of propsSlotScope2.filters"
        :key="filter.value"
        :style="
          value === filter.value
            ? 'color: #1890ff; background-color: #e6f7ff;'
            : ''
        "
        class="ant-dropdown-menu-item-forced ant-dropdown-menu-item radio-block"
        :value="filter.value"
        >{{ filter.textLang ? $t(filter.textLang) : filter.text }}</a-radio
      >
    </a-radio-group>
  </div>
</template>

<script>
import cloneDeep from "lodash.clonedeep";
export default {
  name: "FilterDropdownTable",
  props: ["propsSlotScope", "filterClass"],
  data() {
    return {
      value: "",
    };
  },
  computed: {
    propsSlotScope2() {
      let tempArr = cloneDeep(this.propsSlotScope);
      tempArr.filters.unshift({ value: "", text: "All" });
      return tempArr;
    },
  },
  methods: {
    async handleChangeCheckbox(e) {
      const value = e.target.value;
      await this.propsSlotScope.setSelectedKeys(value ? [value] : []);
      value
        ? this.handleFilter(
            this.propsSlotScope.selectedKeys,
            this.propsSlotScope.confirm
          )
        : this.handleReset(this.propsSlotScope.clearFilters);
    },

    handleFilter(selectedKeys, confirm) {
      confirm();
      this.value = selectedKeys?.[0];
      this.$emit("change", this.value);
    },

    handleReset(clearFilters) {
      clearFilters();
      this.value = "";
      this.$emit("change", this.value);
    },
  },
  mounted() {
    if (
      this.propsSlotScope.selectedKeys &&
      this.propsSlotScope.selectedKeys.length
    ) {
      this.value = this.propsSlotScope.selectedKeys[0];
    }
  },
  watch: {
    "propsSlotScope.selectedKeys"(newVal) {
      if (newVal && newVal.length) this.value = newVal[0];
      else this.value = "";
    },
  },
};
</script>

<style>
.radio-block {
  display: block;
}
.filter-style {
  width: 100%;
  padding: 4px 0px;
}
.filter-credit-status {
  overflow-y: auto;
}
.ant-dropdown-menu-item-forced {
  clear: both;
  margin: 0;
  padding: 5px 12px !important;
  color: rgba(0, 0, 0, 0.65);
  font-weight: normal;
  font-size: 14px;
  line-height: 22px;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.3s;
}
</style>