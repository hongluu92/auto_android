<template>
  <div class="param-column">
    <a-form-model-item
      v-for="(value, param) in paramList"
      :key="param"
      :prop="param"
    >
      <a-tooltip slot="label" :title="value.desc">
        <span
          :class="{
            'cursor-pointer': true,
            'long-text': param == 'removed_background',
          }"
        >
          <a-icon type="question-circle" class="mr-1 hint-icon" />{{ param
          }}{{ param === "removed_background" ? " :" : "" }}</span
        >
      </a-tooltip>

      <a-select
        v-if="param === 'type_converter'"
        class="width-100"
        v-model="form[param]"
        :disabled="isDisabled"
      >
        <a-select-option value="instant_ngp"> instant_ngp </a-select-option>
      </a-select>
      <a-slider
        v-else-if="param === 'scale_percent'"
        v-model="form[param]"
        :max="1"
        :min="0.1"
        :step="0.1"
        :disabled="isDisabled"
      />
      <a-select
        v-else-if="param === 'mode'"
        class="width-100"
        v-model="form[param]"
        :disabled="isDisabled"
      >
        <a-select-option value="nerf"> nerf </a-select-option>
        <a-select-option value="sdf"> sdf </a-select-option>
        <a-select-option value="image"> image </a-select-option>
        <a-select-option value="volume"> volume </a-select-option>
      </a-select>
      <a-select
        v-else-if="param === 'colmap_matcher'"
        class="width-100"
        v-model="form[param]"
        :disabled="isDisabled"
      >
        <a-select-option value="exhaustive"> exhaustive </a-select-option>
        <a-select-option value="sequential"> sequential </a-select-option>
        <a-select-option value="spatial"> spatial </a-select-option>
        <a-select-option value="transitive"> transitive </a-select-option>
        <a-select-option value="vocab_tree"> vocab_tree </a-select-option>
      </a-select>
      <a-slider
        v-else-if="param === 'aabb_scale'"
        v-model="form[param]"
        :marks="{ 1: 1, 2: 2, 4: 4, 8: 8, 16: 16 }"
        :max="16"
        :min="1"
        :step="null"
        :disabled="isDisabled"
      />
      <a-slider
        v-else-if="param === 'exposure'"
        v-model="form[param]"
        :max="4"
        :min="-4"
        :disabled="isDisabled"
      />
      <a-slider
        v-else-if="param === 'sharpen'"
        v-model="form[param]"
        :max="1"
        :min="0"
        :step="0.1"
        :disabled="isDisabled"
      />
      <a-input-number
        v-else-if="value.type === 'float'"
        :max="param === 'sharpen' ? 1 : Infinity"
        :min="param === 'sharpen' ? 0 : -Infinity"
        v-model="form[param]"
        class="width-100"
        :disabled="isDisabled"
      />
      <a-input-number
        v-else-if="value.type === 'interger'"
        v-model="form[param]"
        class="width-100"
        :precision="0"
        :disabled="param === 'n_steps' ? disabled : isDisabled"
      />
      <a-input v-else v-model="form[param]" :disabled="isDisabled" />
    </a-form-model-item>
  </div>
</template>

<script>
export default {
  props: {
    paramList: {
      type: Object,
      default: () => {},
    },
    form: {
      type: Object,
      default: () => {},
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    isDisabled() {
      return this.disabled;
    },
  },
};
</script>

<style>
.param-column .ant-form-item-control {
  line-height: unset;
}
.hint-icon {
  color: #999;
  vertical-align: middle !important;
  margin-bottom: 2px;
}
.cursor-pointer {
  cursor: pointer;
}
.param-column .ant-switch {
  vertical-align: unset;
  margin-top: 7px;
}
.long-text {
  line-height: 0px;
  width: 100%;
  padding: 0;
  overflow: hidden;
  position: relative;
  display: inline-block;
  padding-right: 10px;
  text-decoration: none;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #000;
}
</style>