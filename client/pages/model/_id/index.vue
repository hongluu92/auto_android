<template>
  <a-row v-if="model" :gutter="24" align="middle" justify="start" type="flex">
    <a-col :md="12" :xs="24">
      <a-spin :spinning="isLoading">
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
    </a-col>

    <a-col :md="12" :xs="24">
      <div>
        <a-row class="mb-2">
          <a-col :xs="24" :md="12" class="text-bold">
            {{ model.name }}
          </a-col>

          <a-col :xs="24" :md="12" class="text-right">
            <a-button
              v-if="!didCompleteRemeshing"
              type="primary"
              :loading="isRemeshing"
              @click="handleRemesh"
              >{{ isRemeshing ? "Remeshing" : "Remesh" }}</a-button
            >
            <a-button
              v-if="didCompleteRemeshing"
              type="primary"
              :disabled="isLoading"
              @click="handleViewRemeshedModel"
              >{{
                isViewingRemeshedModel
                  ? "View original model"
                  : "View remeshed model"
              }}</a-button
            >
            <a-button
              v-if="isRemeshing"
              type="danger"
              @click="handleCancelRemesh"
              >Cancel</a-button
            >
          </a-col>
        </a-row>

        <div
          v-for="(value, param) in inputParams"
          :key="param"
          :class="{
            'model-description-item': true,
            'mt-2': true,
            'important-param': param == 'psnr',
          }"
        >
          {{ param == "psnr" ? "PSNR" : snakeCaseToTitleCase(param) }}
          <a-tooltip
            slot="label"
            :title="'The ratio between the maximum possible power of an image and the power of corrupting noise that affects the quality of its representation'"
          >
            <a-icon
              v-if="param == 'psnr'"
              type="question-circle"
              class="mr-1 hint-icon"
            />
          </a-tooltip>
          <span
            :class="{
              'float-right': true,
              'text-danger': param == 'psnr' && value < 40,
              'text-success': param == 'psnr' && value >= 40,
            }"
            >{{ value }}</span
          >
        </div>
      </div>
    </a-col>
  </a-row>
</template>

<script>
const refreshInterval = 5000;
import { ModelPly } from "vue-3d-model";
import baseMixin from "@/mixins/baseMixin";
import modelMixin from "@/mixins/modelMixin";
import { mapState, mapActions } from "vuex";
const lightStrength = 0.5;
export default {
  name: "3dModel",
  mixins: [baseMixin, modelMixin],
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
      hasStartedRemeshing: false,
      isViewingRemeshedModel: false,
    };
  },
  computed: {
    ...mapState(["model"]),
    modelId() {
      return this.$route.params.id;
    },
    configId() {
      return this.$route.query.configId;
    },
    modelSource() {
      return `${process.env.API_BASE_URL}/data_processed/${this.modelId}/nerf/${
        this.configId
      }/result/${this.isViewingRemeshedModel ? "remesh" : "point_cloud"}.ply`;
    },
    inputParams() {
      if (!this.currentParamConfig) return {};
      let mergedParamList = {};

      let metaData = this.currentParamConfig.meta_data;
      if (metaData) {
        mergedParamList = {
          ...mergedParamList,
          ...metaData,
        };
      }

      // add output_file_size or remeshed_output_file_size to the list
      let fileSize = this.isViewingRemeshedModel
        ? this.currentParamConfig.remeshed_output_file_size
        : this.currentParamConfig.output_file_size;
      // convert to readable format
      if (fileSize > 1024 * 1024) {
        fileSize = `${(fileSize / 1024 / 1024).toFixed(2)} MB`;
      } else if (fileSize > 1024) {
        fileSize = `${(fileSize / 1024).toFixed(2)} KB`;
      } else {
        fileSize = `${fileSize} B`;
      }
      mergedParamList["output_file_size"] = fileSize;

      for (let paramType in this.currentParamConfig.parameter_json_data) {
        mergedParamList = {
          ...mergedParamList,
          ...this.currentParamConfig.parameter_json_data[paramType],
        };
      }

      // Exclude videoOnly params if the model type is image
      let videoOnlyParams = ["video_fps", "time_slice"];
      if (this.model?.type === "image") {
        videoOnlyParams.forEach((param) => {
          delete mergedParamList[param];
        });
      }

      return mergedParamList;
    },
    isRemeshing() {
      if (this.hasStartedRemeshing) return true;
      if (!this.configId) return false;
      if (!this.model?.trainingParams) return false;
      let config = this.model.trainingParams.find(
        (config) => config.id == this.configId
      );
      if (!config) return false;
      return config.status === "remeshing";
    },
    didCompleteRemeshing() {
      if (!this.configId) return false;
      if (!this.model?.trainingParams) return false;
      let config = this.model.trainingParams.find(
        (config) => config.id == this.configId
      );
      if (!config) return false;
      return config.status === "remeshed";
    },
  },
  methods: {
    ...mapActions(["getModelById", "remesh", "cancelModel"]),
    updateModelSize() {
      let heightOffset = 150;
      let widthOffset = 70;

      if (this.isMobile) {
        this.height = window.innerHeight - heightOffset;
      } else {
        this.height = window.innerHeight - heightOffset * 2;
      }

      if (this.isMobile) this.width = window.innerWidth - widthOffset;
      else this.width = window.innerWidth / 2 - widthOffset;
    },
    onLoad() {
      this.isLoading = false;
    },
    onProgress() {
      this.isLoading = true;
    },
    async handleRemesh() {
      this.hasStartedRemeshing = true;
      await this.remesh(this.configId);
      this.hasStartedRemeshing = false;
      this.refreshModelStatusEveryMilisecs(refreshInterval);
    },
    async refreshModelStatusEveryMilisecs(interval) {
      await this.refreshModelStatus();
      this.interval = setInterval(this.refreshModelStatus, interval);
    },
    async refreshModelStatus() {
      await this.getModelById(this.modelId);

      if (!this.isRemeshing) {
        clearInterval(this.interval);
      }
    },
    async handleCancelRemesh() {
      this.hasStartedRemeshing = false;
      await this.cancelModel({ configId: this.configId, isRemeshing: true });
      this.refreshModelStatus();
    },
    handleViewRemeshedModel() {
      this.isViewingRemeshedModel = !this.isViewingRemeshedModel;
    },
  },
  async created() {
    await this.getModelById(this.modelId);
    if (!this.model) {
      window.history.back();
    } else {
      this.updateModelSize();
      if (this.isRemeshing) {
        this.refreshModelStatusEveryMilisecs(refreshInterval);
      }
    }
  },
};
</script>

<style>
.model-description-item {
  border-bottom: 1px solid #e8e8e8;
}

.important-param {
  font-weight: bold;
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