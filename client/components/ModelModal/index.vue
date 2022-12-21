<template>
  <a-modal
    :footer="false"
    visible
    @cancel="$emit('cancel')"
    centered
    :width="1200"
    destroyOnClose
  >
    <a-spin :spinning="isLoading" class="text-center">
      <model-ply
        v-if="height"
        :src="modelSource"
        :height="height"
        :width="width || undefined"
        :lights="lights"
        @on-load="onLoad"
        @on-progress="onProgress"
      ></model-ply>
    </a-spin>
  </a-modal>
</template>

<script>
import { ModelPly } from "vue-3d-model";
import baseMixin from "@/mixins/baseMixin";
const lightStrength = 0.5;
export default {
  name: "Step4",
  mixins: [baseMixin],
  props: ["modelId", "configId"],
  components: { ModelPly },
  data() {
    return {
      height: 0,
      width: 0,
      hasTouchScreen: false,
      isLoading: false,
      lights: [
        {
          type: "DirectionalLight",
          position: { x: 1, y: 1, z: 1 },
          color: 0xffffff,
          intensity: lightStrength,
        },
        {
          type: "DirectionalLight",
          position: { x: -1, y: 1, z: 1 },
          color: 0xffffff,
          intensity: lightStrength,
        },
        {
          type: "DirectionalLight",
          position: { x: 1, y: 1, z: -1 },
          color: 0xffffff,
          intensity: lightStrength,
        },
        {
          type: "DirectionalLight",
          position: { x: -1, y: 1, z: -1 },
          color: 0xffffff,
          intensity: lightStrength,
        },
        {
          type: "DirectionalLight",
          position: { x: 0, y: -1, z: 0 },
          color: 0xffffff,
          intensity: lightStrength,
        },
      ],
    };
  },
  computed: {
    modelSource() {
      return `${process.env.API_BASE_URL}/data_processed/${this.modelId}/nerf/${this.configId}/result/point_cloud.ply`;
    },
  },
  methods: {
    updateModelSize() {
      let heightOffset = 150;
      let widthOffset = 70;

      if (this.hasTouchScreen) {
        this.height = window.innerHeight - heightOffset;
      } else {
        this.height = window.innerHeight - heightOffset * 2;
      }

      if (this.hasTouchScreen) this.width = window.innerWidth - widthOffset;
      else this.width = window.innerWidth / 2 - widthOffset;
    },
    onLoad() {
      this.isLoading = false;
    },
    onProgress() {
      this.isLoading = true;
    },
  },
  async created() {},
  mounted() {
    this.checkIfDeviceHasTouchScreen();
    this.updateModelSize();
  },
};
</script>

<style>
.model-description-item {
  border-bottom: 1px solid #e8e8e8;
}

@media only screen and (min-width: 825px) {
  .text-bottom {
    position: absolute;
    bottom: 80px;
    width: 100%;
  }
}

@media only screen and (max-width: 824px) {
  .text-bottom {
    width: 100%;
    margin-top: 1rem !important;
  }
}
</style>