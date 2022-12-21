<template>
  <div>
    <a-row :gutter="24" type="flex" justify="space-between" align="top">
      <a-col :md="16" :xs="24" class="param-col mb-2">
        <a-steps
          v-if="areImagesSelectable"
          class="max-width-400px mb-3"
          v-model="currentStep"
          @change="handleStepChange"
        >
          <a-step
            title="Pose Estimation"
            :disabled="isProcessingAnyModel || type == '3dImage'"
          />
          <a-step
            title="3D Reconstruction"
            :disabled="
              (!didExtractPoses && !didUploadPoses) || isProcessingAnyModel
            "
          />
        </a-steps>

        <a-checkbox
          v-if="currentStep === 0"
          class="mb-2"
          v-model="shouldUploadPoses"
        >
          Upload camera poses
        </a-checkbox>

        <a-button
          v-if="currentStep === 1"
          type="primary"
          ghost
          icon="plus"
          class="mb-2"
          :disabled="hasAnyNewConfig"
          @click="handleAddConfig"
        >
          New config</a-button
        >
        <a-table
          v-if="
            model && didFetchModel && (currentStep === 1 || !shouldUploadPoses)
          "
          class="outer-table"
          :columns="columns"
          :dataSource="trainingParams"
          :pagination="false"
          :showHeader="false"
          :scroll="{ x: true }"
          :rowKey="(record) => record.id"
          :expandedRowKeys="expandedRowKeys"
        >
          <template slot="expandIcon" slot-scope="props"> </template>
          <template slot="configName" slot-scope="text, record">
            {{ getConfigName(record) }}
          </template>
          <template slot="expandedRowRender" slot-scope="record">
            <a-form-model
              v-if="form[record.id] && form[record.id].isEditing"
              class="param-form"
              v-bind="formLayout"
              layout="horizontal"
              :model="form"
              :rules="rules"
              ref="templateForm"
            >
              <ParamColumn
                :paramList="getParamColumns(true)"
                :form="form[record.id]"
                :disabled="isUnzipping"
              />
            </a-form-model>
            <a-table
              v-else-if="form[record.id]"
              class="fixed-width-table"
              :columns="getParamColumns()"
              :dataSource="[{}]"
              :pagination="false"
              :rowKey="(r, i) => i"
              :scroll="{ x: true }"
            >
              <template v-for="column in getParamColumns()" :slot="column.key">
                <span v-if="column.key != 'n_steps'" :key="column.key">
                  {{ form[record.id][column.dataIndex] }}
                </span>
                <a-input-number
                  v-else-if="column.key == 'n_steps'"
                  :key="column.key"
                  v-model="form[record.id].n_steps"
                  :disabled="isProcessing(record)"
                  :precision="0"
                />
              </template>
            </a-table>

            <a-steps
              v-if="record.steps"
              :current="99"
              class="steps"
              :style="`max-width: ${record.steps.length * 250}px`"
            >
              <a-step
                v-for="step in record.steps"
                :key="step.id"
                :status="getStepStatus(step.status)"
              >
                <template slot="title"> {{ step.name }} </template>
                <span slot="description">{{ step.desc }}</span>
              </a-step>
            </a-steps>
          </template>

          <div
            v-if="!isUnzipping"
            slot="status"
            slot-scope="text, record"
            class="text-right"
          >
            <a-button
              v-if="
                !isProcessing(record) &&
                form[record.id] &&
                !form[record.id].isEditing
              "
              type="primary"
              @click="handleEditConfig(record)"
              >Edit config</a-button
            >
            <a-button
              v-if="form[record.id] && form[record.id].isEditing"
              type="primary"
              @click="cancelEditConfig(record)"
              >Cancel</a-button
            >
            <a-button
              v-if="!isProcessing(record)"
              type="danger"
              @click="handleDeleteConfig(record)"
              >Delete</a-button
            >
            <a-button
              v-if="isProcessingCompleted(record)"
              type="primary"
              @click="handleProcessBtnClick(record, false, true)"
              :loading="isProcessing(record)"
              :disabled="isRemovingBackground"
              >Re-run</a-button
            >
            <a-button
              v-if="isProcessingCompleted(record)"
              type="primary"
              @click="handleProcessBtnClick(record, true)"
              :loading="isProcessing(record)"
              :disabled="isRemovingBackground"
              >Continue training</a-button
            >
            <a-button
              v-if="isRemeshing(record)"
              type="primary"
              @click="viewModel(record)"
              >View 3D model</a-button
            >
            <a-button
              type="primary"
              @click="handleProcessBtnClick(record)"
              :loading="isProcessing(record)"
              :disabled="isRemovingBackground || isQueued(record)"
              >{{ getButtonTitle(record) }}</a-button
            >
            <a-button
              v-if="isProcessing(record)"
              type="danger"
              :loading="isCanceling"
              @click="handleCancel(record)"
              >Cancel</a-button
            >
          </div>
        </a-table>

        <div v-else-if="shouldUploadPoses" class="text-center">
          <a-upload
            :accept="'.json'"
            :file-list="fileList"
            :listType="'text'"
            :before-upload="beforeUpload"
            :remove="handleRemove"
          >
            <a-button type="primary" ghost>
              <a-icon type="upload" /><span> Select file</span>
            </a-button>
          </a-upload>

          <a-button
            v-if="fileList.length > 0"
            type="primary"
            class="mt-2"
            @click="handleUpload"
            :loading="uploading"
            >Upload</a-button
          >
        </div>
      </a-col>
      <a-col :md="8" :xs="24">
        <div class="image-list-container mb-1" v-if="model && didFetchModel">
          <a-row
            class="mb-2"
            type="flex"
            justify="space-between"
            align="middle"
          >
            <a-col
              v-if="!isProcessingAnyModel"
              :xs="24"
              :md="10"
              class="text-left"
            >
              <a-tooltip
                v-if="areImagesSelectable && currentStep === 0"
                title="Select files for deletion"
                :arrowPointAtCenter="true"
                placement="bottom"
                :getPopupContainer="(a) => a.parentNode"
              >
                <a-button
                  class="mb-1"
                  type="primary"
                  ghost
                  @click="handleClickSelectAll"
                  >Select all ({{ files.length }})</a-button
                >
              </a-tooltip>
              <a-button
                v-if="selectedFiles.length && !isProcessingAnyModel"
                type="danger"
                :loading="isDeletingFiles"
                @click="handleDeleteSelectedFiles"
              >
                Delete</a-button
              >
            </a-col>
            <a-col
              v-else-if="!shouldExtractImages"
              :xs="24"
              :md="10"
              class="text-left"
            >
              Total: {{ files.length }} images
            </a-col>
            <a-col :xs="24" :md="14" class="text-right">
              <a-checkbox
                v-if="!isProcessingAnyModel && areImagesSelectable"
                :checked="shouldRemoveBackgroundBeChecked"
                :disabled="isRemovingBackground"
                @change="handleRemoveBackground"
              >
                Remove background
              </a-checkbox>
              <a-button
                v-if="didExtractImages"
                class="width-100px"
                type="primary"
                @click="handleViewVideo"
              >
                Video</a-button
              >
            </a-col>
          </a-row>
          <a-spin
            :spinning="
              estimatedTime != '00:00' || isRemovingBackground || isUnzipping
            "
            :tip="
              estimatedTime != '00:00'
                ? `Estimated remaining time: ${estimatedTime} seconds`
                : isUnzipping
                ? 'Unzipping...'
                : ''
            "
          >
            <FileList
              :files="files"
              viewMode="grid"
              :type="didExtractImages || type === '3dImage' ? 'image' : type"
              :maxGridCols="2"
              :shouldShowCheckbox="!isProcessingAnyModel && currentStep === 0"
              :checkedFiles="selectedFiles"
              @checkboxChange="(val, item) => handleCheckboxChange(val, item)"
            />
          </a-spin>
        </div>
      </a-col>
    </a-row>

    <PreviewModal
      v-if="showPreviewModal"
      :files="originalFiles"
      :modelId="previewingModelName"
      :type="'video'"
      :shouldRenderExtractImagesButton="!isProcessingAnyModel"
      @extractImages="handleExtractImagesAgain"
      @cancel="handleCancelPreview"
    />
  </div>
</template>
<script>
const refreshInterval = 5000;
import { mapState, mapActions, mapMutations } from "vuex";
import * as CONST from "@/constants/index.js";
import ParamColumn from "@/components/ParamColumn";
import FileList from "@/components/FileList";
import PreviewModal from "@/components/PreviewModal";
import { columns } from "./const";
import modelMixin from "@/mixins/modelMixin";
export default {
  mixins: [modelMixin],
  components: {
    ParamColumn,
    FileList,
    PreviewModal,
  },
  data() {
    return {
      CONST,
      totalSteps: 0,
      form: {},
      rules: {},
      formLayout: {
        labelCol: { xs: { span: 24 }, sm: { span: 4 } },
        wrapperCol: { xs: { span: 24 }, sm: { span: 10 } },
      },
      hasStartedProcessingConfigId: null,
      isCanceling: false,
      didFetchModel: false,
      isRemovingBackground: false,
      selectedFiles: [],
      isDeletingFiles: false,
      configId: "new",
      showPreviewModal: false,
      originalFiles: [],
      previewingModelName: "",
      columns,
      estimatedTime: "00:00",
      viewingModelId: null,
      viewingConfigId: null,
      shouldExtractImagesAgain: false,
      isUnzipping: false,
      currentStep: 0,
      overiddenRemovedBackground: undefined,
      shouldUploadPoses: false,
      fileList: [],
      uploading: false,
    };
  },
  computed: {
    ...mapState(["paramList", "model"]),
    modelId() {
      return this.$route.params.id;
    },
    files() {
      if (!this.model) return [];

      let files = [];
      if (this.shouldExtractImagesAgain) {
        files = this.model.originalFiles ?? this.model.files ?? [];
      } else if (this.shouldRemoveBackgroundBeChecked) {
        let skipCharCount =
          this.type === "image" ? 22 : this.type === "video" ? 29 : 37;
        // replace the first skipCharCount to /data_processed/{modelId}/images/rmbg for each file
        files = this.model.files.map((file) => {
          return file.replace(
            file.substring(0, skipCharCount),
            `/data_processed/${this.modelId}/images/rmbg`
          );
        });
      } else {
        files = this.model.files;
      }

      return files;
    },
    type() {
      return this.model?.type;
    },
    didExtractImages() {
      if (this.shouldExtractImagesAgain) return false;
      if (!this.model) return false;
      if (!this.model.trainingParams) return false;
      let didExtractImagesIn1stConfig =
        this.model.trainingParams[0]?.parameter_json_data?.common
          ?.did_extract_images;

      return didExtractImagesIn1stConfig;
    },
    didRemoveBackground() {
      if (!this.model) return false;
      if (!this.model.trainingParams) return false;
      let config = this.model?.trainingParams?.find((config) =>
        [true, false].includes(
          config.parameter_json_data?.common?.did_extract_poses
        )
      );
      if (!config) return false;
      return config.parameter_json_data?.common?.removed_background;
    },
    shouldRemoveBackgroundBeChecked() {
      if (this.overiddenRemovedBackground !== undefined) {
        return this.overiddenRemovedBackground;
      }
      return this.didRemoveBackground;
    },
    didExtractPoses() {
      if (!this.model) return false;
      if (!this.model.trainingParams) return false;
      let didExtractPosesInAnyConfig = this.model.trainingParams.some(
        (config) => {
          return config.parameter_json_data?.common?.did_extract_poses;
        }
      );
      return didExtractPosesInAnyConfig && !this.didFailExtractingPoses;
    },
    didUploadPoses() {
      if (!this.model) return false;
      if (!this.model.trainingParams) return false;
      let didUploadPosesInAnyConfig = this.model.trainingParams.some(
        (config) => {
          return config.parameter_json_data?.common?.did_upload_poses;
        }
      );
      return didUploadPosesInAnyConfig;
    },
    didFailExtractingPoses() {
      if (!this.model) return false;
      if (!this.model.trainingParams) return false;
      let didFailExtractingPosesInAnyConfig =
        this.model.trainingParams.find((config) => {
          return [true, false].includes(
            config.parameter_json_data?.common?.did_extract_poses
          );
        })?.status === "failed";

      return didFailExtractingPosesInAnyConfig;
    },
    shouldExtractImages() {
      return !this.didExtractImages && this.type === "video";
    },
    shouldExtractPoses() {
      return (
        !this.shouldExtractImages &&
        this.type != "3dImage" &&
        this.currentStep === 0
      );
    },
    isProcessingAnyModel() {
      return this.trainingParams?.some((config) => this.isProcessing(config));
    },
    expandedRowKeys() {
      return this.trainingParams?.map((config) => config.id);
    },
    hasAnyNewConfig() {
      return this.trainingParams?.some((config) => config.id === "new");
    },
    hasAnyConfig() {
      return this.trainingParams?.length > 0 || this.hasAnyNewConfig;
    },
    onlyHasNewConfig() {
      return this.trainingParams?.length === 1 && this.hasAnyNewConfig;
    },
    isFromUpload() {
      return this.$route.params.isFromUpload;
    },
    trainingParams() {
      let trainingParams = this.model?.trainingParams;

      let configs = this.shouldExtractImages
        ? trainingParams?.slice(0, 1)
        : this.shouldExtractPoses || this.currentStep === 0
        ? this.type === "video"
          ? trainingParams?.slice(1, 2)
          : trainingParams?.slice(0, 1)
        : this.type === "video"
        ? trainingParams?.slice(2)
        : this.type === "image"
        ? trainingParams?.slice(1)
        : trainingParams;

      return configs;
    },
    areImagesSelectable() {
      return (
        !this.isUnzipping &&
        (["image", "3dImage"].includes(this.type) || this.didExtractImages)
      );
    },
    isExtractingPoses() {
      return (
        this.model?.trainingParams?.find((config) => {
          return [true, false].includes(
            config.parameter_json_data?.common?.did_extract_poses
          );
        })?.status === "processing"
      );
    },
  },
  async created() {
    await this.getModelById(this.modelId);
    if (!this.model) {
      window.history.back();
      return;
    }
    this.didFetchModel = true;
    await this.fetchParamList();

    this.initParams();
  },
  methods: {
    ...mapActions([
      "fetchScriptList",
      "fetchParamList",
      "updateModel",
      "processModel",
      "getModelById",
      "cancelModel",
      "continueProcessingModel",
      "removeBackground",
      "deleteImages",
      "extractImages",
      "unzip",
      "getEstimatedTime",
      "deleteConfig",
      "extractPoses",
      "uploadPoses",
    ]),
    ...mapMutations(["setCurrentModel"]),
    initParams(shouldNotAutoTransition = false) {
      if (!shouldNotAutoTransition) {
        if (
          this.isExtractingPoses ||
          ((this.didFailExtractingPoses || !this.didExtractPoses) &&
            !this.didUploadPoses &&
            this.type !== "3dImage")
        ) {
          this.currentStep = 0;
        } else this.currentStep = 1;
      }

      this.form = {};
      this.model.trainingParams.forEach((config, index) => {
        this.$set(this.form, config.id, { isEditing: false });

        if (config.parameter_json_data) {
          this.setModelParams(config);
          if (this.isProcessing(config))
            this.refreshModelStatusEveryMilisecs(refreshInterval);
        } else this.setDefaultParams(config, index);
      });

      if (!this.hasAnyConfig) {
        this.handleAddConfig();
        this.handleEditConfig({ id: "new" });

        let shouldExtractImages =
          this.type === "video" && this.isFromUpload && !this.didExtractImages;
        let shouldUnzipImages =
          this.type === "3dImage" &&
          this.isFromUpload &&
          !this.model.files.length &&
          !this.didExtractPoses;

        if (shouldExtractImages || shouldUnzipImages) {
          let config = this.trainingParams[0];
          if (shouldExtractImages) this.handleProcessBtnClick(config);
          else if (shouldUnzipImages)
            this.handleProcessBtnClick(config, false, false, true);
        }
      } else if (this.onlyHasNewConfig) {
        this.setDefaultParams(this.trainingParams[0]);
        this.handleEditConfig({ id: "new" });
      }
    },
    setDefaultParams(config) {
      for (const paramType in this.paramList) {
        for (const param in this.paramList[paramType]) {
          let default_val = this.paramList[paramType][param].default_val;

          if (config.id === "new" && param === "name") {
            let index = this.trainingParams.length;
            if (this.onlyHasNewConfig) index -= 1;
            default_val = `config_${index + 1}`;
            this.$set(this.form[config.id], param, default_val);
          } else if (this.paramList[paramType][param].type === "float") {
            this.$set(this.form[config.id], param, parseFloat(default_val));
          } else if (this.paramList[paramType][param].type === "interger") {
            this.$set(this.form[config.id], param, parseInt(default_val));
          } else {
            this.$set(this.form[config.id], param, default_val);
          }
        }
      }
    },
    setModelParams(config) {
      for (const paramType in config.parameter_json_data) {
        for (const param in config.parameter_json_data[paramType]) {
          this.$set(
            this.form[config.id],
            param,
            config.parameter_json_data[paramType][param]
          );
        }
      }
    },
    async handleProcessBtnClick(
      config,
      shouldContinueTraining,
      shouldRerun,
      shouldUnzip
    ) {
      if (shouldContinueTraining) {
        await this.handleContinueTraining(config);
        return;
      }

      // If the processing is in progress, do nothing
      if (this.isProcessing(config)) {
        return;
      }

      // If the processing is completed, redirect to 3D model page
      if (this.isProcessingCompleted(config) && !shouldRerun) {
        this.viewModel(config);
        return;
      }

      // If the user extracts images from video, set the did_extract_images param to true and call the extractImages action
      if (this.shouldExtractImages) {
        await this.handleExtractImages(config);
        return;
      }

      // if the user unzips images, call the unzip action
      if (shouldUnzip) {
        await this.handleUnzipImages(config);
        return;
      }

      // if the user extracts poses, call the extractPoses action
      if (this.shouldExtractPoses) {
        await this.handleExtractPoses(config);
        return;
      }

      this.$set(this.form[config.id], "isEditing", false);
      let configId = await this.updateModelParams(config);
      this.handleProcessing(configId ? { id: configId } : config);
    },
    async handleContinueTraining(config) {
      this.$set(this.form[config.id], "isEditing", false);
      this.hasStartedProcessingConfigId = config.id;
      try {
        await this.continueProcessingModel({
          configId: config.id,
          n_steps: this.form[config.id].n_steps,
        });
        this.refreshModelStatusEveryMilisecs(refreshInterval);
      } catch (error) {
        this.handleProcessingError(error);
      }
    },
    viewModel(config) {
      // open 3D model page in new popup window with 1/3 width of the screen
      let width = window.innerWidth / 3;
      let height = window.innerHeight;
      let left = window.innerWidth / 2 - width / 2;
      let top = window.innerHeight / 2 - height / 2;
      window.open(
        `/model/${this.modelId}?configId=${config.id}`,
        "_blank",
        `location=yes,width=${width},height=${height},left=${left},top=${top},scrollbars=yes,status=yes`
      );
    },
    async handleExtractImages(config) {
      let newConfigId;
      try {
        this.$set(this.form[config.id], "isEditing", false);
        this.hasStartedProcessingConfigId = config.id;
        newConfigId = await this.updateModelParams(
          config,
          false,
          false,
          false,
          true
        );
        if (newConfigId) this.hasStartedProcessingConfigId = newConfigId;
        await this.extractImages(config.model_id);

        if (!this.didExtractImages)
          await this.updateModelParams(
            newConfigId ? { id: newConfigId } : config,
            false,
            true,
            false,
            true
          );
        this.shouldExtractImagesAgain = false;
        if (!this.onlyHasNewConfig && this.didRemoveBackground) {
          // update remove_background param to false
          await this.updateBackgroundRemovedStatus();
        }

        await this.refreshModelStatus();
        this.initParams();
        this.$notification.success({
          message: "Success",
          description: "Images extracted successfully",
        });
      } catch (error) {
        this.$notification.error({
          message: "Error",
          description: error.response.data.message,
        });
        this.refreshModelStatus();
      } finally {
        this.hasStartedProcessingConfigId = null;
      }
    },
    async handleExtractPoses(config) {
      let newConfigId;
      try {
        this.$set(this.form[config.id], "isEditing", false);
        this.hasStartedProcessingConfigId = config.id;
        newConfigId = await this.updateModelParams(
          config,
          false,
          false,
          false,
          false,
          true
        );
        if (newConfigId) this.hasStartedProcessingConfigId = newConfigId;
        await this.extractPoses(newConfigId ?? config.id);
        this.refreshModelStatusEveryMilisecs(refreshInterval);
        if (!this.didExtractPoses)
          await this.updateModelParams(
            newConfigId ? { id: newConfigId } : config,
            false,
            false,
            true,
            false,
            true
          );
      } catch (error) {
        this.$notification.error({
          message: "Error",
          description: error.response.data.message,
        });
        await this.deleteConfig(newConfigId ?? config.id);
        await this.refreshModelStatus();
        this.initParams();
      } finally {
        this.hasStartedProcessingConfigId = null;
      }
    },
    async handleUnzipImages(config) {
      try {
        this.isUnzipping = true;
        await this.unzip(config.model_id);

        await this.refreshModelStatus();
        this.initParams();
        this.$notification.success({
          message: "Success",
          description: "Images unzipped successfully",
        });
      } catch (error) {
        this.$notification.error({
          message: "Error",
          description: error.response.data.message,
        });
        this.refreshModelStatus();
      } finally {
        this.isUnzipping = null;
      }
    },
    async updateModelParams(
      config,
      shouldUpdateRemovedBackground = false,
      shouldUpdateDidExtractImages = false,
      shouldUpdateDidExtractPoses = false,
      shouldExtractImagesOnly = false,
      shouldExtractPosesOnly = false,
      shouldDidUploadPosedBeFalse = false
    ) {
      let form = this.form[config.id];

      let parameter_json_data = {};
      if (shouldExtractImagesOnly) {
        parameter_json_data = {
          common: {
            did_extract_images: shouldUpdateDidExtractImages
              ? !this.didExtractImages
              : this.didExtractImages,
          },
          extract: {
            video_fps: form.video_fps,
            time_slice: form.time_slice,
          },
        };
      } else if (shouldExtractPosesOnly) {
        parameter_json_data = {
          common: {
            scale_percent: form.scale_percent,
            removed_background: shouldUpdateRemovedBackground
              ? !this.shouldRemoveBackgroundBeChecked
              : this.shouldRemoveBackgroundBeChecked,
            did_extract_poses: shouldUpdateDidExtractPoses
              ? !this.didExtractPoses
              : this.didExtractPoses,
            did_upload_poses: shouldDidUploadPosedBeFalse
              ? false
              : this.didUploadPoses
              ? true
              : this.shouldUploadPoses,
          },
          extract: {
            colmap_matcher: form.colmap_matcher,
            aabb_scale: form.aabb_scale,
          },
        };
      } else {
        parameter_json_data = {
          common: {
            name: form.name,
            type_converter: form.type_converter,
            scale_percent: form.scale_percent,
            removed_background: this.shouldRemoveBackgroundBeChecked,
          },
          "instant-ngp": {
            mode: form.mode,
            near_distance: form.near_distance,
            exposure: form.exposure,
            n_steps: form.n_steps,
            sharpen: form.sharpen,
          },
        };
      }
      let payload = {
        id: this.modelId,
        metaId: config.id,
        meta: {
          parameter_json_data: parameter_json_data,
        },
      };
      let res = await this.updateModel(payload);
      if (config.id === "new") {
        let configs = res.data[0]?.trainingParams ?? [];
        let newConfigId = configs.find(
          (p) => p.id === Math.max(...configs.map((p) => p.id))
        )?.id;
        this.initParams();
        return newConfigId;
      }
    },
    async handleProcessing(config) {
      try {
        this.hasStartedProcessingConfigId = config.id;
        await this.processModel(config.id);
        this.refreshModelStatusEveryMilisecs(refreshInterval);
      } catch (error) {
        this.handleProcessingError(error);
      }
    },
    handleProcessingError(error) {
      this.$notification.info({
        message: "Queued",
        description: error.response.data.message,
      });
      this.refreshModelStatus();
      this.resetVars();
    },
    async refreshModelStatusEveryMilisecs(interval) {
      await this.refreshModelStatus();
      this.interval = setInterval(this.refreshModelStatus, interval);
    },
    async refreshModelStatus(shouldNotAutoTransition = false) {
      await this.getModelById(this.modelId);
      let hasQueuedConfig = this.trainingParams.find((p) =>
        p.status.includes(CONST.MODEL_STATUS.QUEUED.label)
      );
      if (this.isProcessingAnyModel) this.hasStartedProcessingConfigId = null;
      if (!this.isProcessingAnyModel && !hasQueuedConfig) {
        this.resetVars();
        if (!shouldNotAutoTransition && !this.didFailExtractingPoses)
          if (this.currentStep == 0) {
            this.currentStep = 1;
            this.initParams();
          }
      }
    },
    async handleCancel(config) {
      this.isCanceling = true;
      await this.cancelModel({
        configId: config.id,
        isRemeshing: this.isRemeshing(config),
      });
      if (this.currentStep === 0 && this.didExtractPoses)
        await this.updateModelParams(config, false, false, true, false, true);

      await this.refreshModelStatus(this.currentStep === 0 ? true : false);
      let hasQueuedConfig = this.trainingParams.find((p) =>
        p.status.includes(CONST.MODEL_STATUS.QUEUED.label)
      );
      this.isCanceling = false;
      this.$notification.success({
        message: "Success",
        description: "Canceled successfully.",
      });
      if (hasQueuedConfig)
        this.refreshModelStatusEveryMilisecs(refreshInterval);
      else this.resetVars();
    },
    resetVars() {
      this.hasStartedProcessingConfigId = null;
      clearInterval(this.interval);
    },
    handleCheckboxChange(value, file) {
      let fileName = file.split("/").pop();
      if (value) {
        this.selectedFiles.push(fileName);
      } else {
        this.selectedFiles = this.selectedFiles.filter(
          (selectedFile) => selectedFile !== fileName
        );
      }
    },
    handleClickSelectAll() {
      // If all files are selected, deselect all files
      if (this.selectedFiles.length === this.files.length) {
        this.selectedFiles = [];
        return;
      }

      // If not all files are selected, select all files
      this.selectedFiles = this.files.map((file) => file.split("/").pop());
    },
    handleDeleteSelectedFiles() {
      this.$confirm({
        title: "Are you sure you want to delete the selected files?",
        content: "This action cannot be undone.",
        okText: "Yes",
        okType: "danger",
        cancelText: "No",
        centered: true,
        onOk: async () => {
          try {
            this.isDeletingFiles = true;
            let payload = {
              id: this.modelId,
              files: this.selectedFiles,
            };
            await this.deleteImages(payload);
            if (this.currentStep === 0 && this.didExtractPoses) {
              let config = this.trainingParams[0];
              await this.updateModelParams(
                config,
                false,
                false,
                true,
                false,
                true
              );
            }

            this.$notification.success({
              message: "Success",
              description: "The files were deleted successfully.",
            });
            this.selectedFiles = [];
            await this.refreshModelStatus();
          } catch (error) {
            this.$notification.error({
              message: "Error",
              description: error.response.data.message,
            });
          } finally {
            this.isDeletingFiles = false;
          }
        },
      });
    },
    handleViewVideo() {
      this.showPreviewModal = true;
      this.originalFiles = this.model.originalFiles;
      this.previewingModelName = this.model.name;
    },
    handleCancelPreview() {
      this.showPreviewModal = false;
    },
    getParamColumns(shouldReturnObject = false) {
      // Merge all paramList into one object
      let mergedParamList = {};
      for (let paramType in this.paramList) {
        mergedParamList = {
          ...mergedParamList,
          ...this.paramList[paramType],
        };
      }

      // Exclude videoOnly params if the model type is image
      let videoOnlyParams = ["video_fps", "time_slice"];
      if (this.model?.type == "image") {
        mergedParamList = Object.keys(mergedParamList).reduce((acc, cur) => {
          if (!videoOnlyParams.includes(cur)) {
            acc[cur] = mergedParamList[cur];
          }
          return acc;
        }, {});
      }

      // Exclude param named "did_extract_images" or "removed_background" or "apply_for"
      mergedParamList = Object.keys(mergedParamList).reduce((acc, cur) => {
        if (
          cur != "did_extract_images" &&
          cur != "removed_background" &&
          cur != "apply_for"
        ) {
          acc[cur] = mergedParamList[cur];
        }
        return acc;
      }, {});

      // If shouldExtractImages is true, exclude all params except "video_fps" and "time_slice" (if model type is video)
      if (this.shouldExtractImages) {
        mergedParamList = Object.keys(mergedParamList).reduce((acc, cur) => {
          if (videoOnlyParams.includes(cur)) {
            acc[cur] = mergedParamList[cur];
          }
          return acc;
        }, {});
      }

      // If didExtractImages is true, exclude "video_fps" and "time_slice" (if model type is video)
      if (this.didExtractImages || this.type === "3dImage") {
        mergedParamList = Object.keys(mergedParamList).reduce((acc, cur) => {
          if (!videoOnlyParams.includes(cur)) {
            acc[cur] = mergedParamList[cur];
          }
          return acc;
        }, {});
      }

      let step1Params = ["colmap_matcher", "aabb_scale"];
      let commonParams = ["scale_percent"];
      let extractImagesParams = ["video_fps", "time_slice"];

      if (this.shouldExtractImages) {
        mergedParamList = Object.keys(mergedParamList).reduce((acc, cur) => {
          if (extractImagesParams.includes(cur)) {
            acc[cur] = mergedParamList[cur];
          }
          return acc;
        }, {});
      } else if (this.currentStep == 0) {
        mergedParamList = Object.keys(mergedParamList).reduce((acc, cur) => {
          if (step1Params.includes(cur) || commonParams.includes(cur)) {
            acc[cur] = mergedParamList[cur];
          }
          return acc;
        }, {});
      } else if (this.currentStep == 1) {
        mergedParamList = Object.keys(mergedParamList).reduce((acc, cur) => {
          if (!step1Params.includes(cur) || commonParams.includes(cur)) {
            acc[cur] = mergedParamList[cur];
          }
          return acc;
        }, {});
      }

      if (shouldReturnObject) {
        return mergedParamList;
      }

      let columns = [];

      columns = Object.keys(mergedParamList).map((param) => {
        return {
          title: this.snakeCaseToTitleCase(param),
          dataIndex: param,
          key: param,
          scopedSlots: { customRender: param },
        };
      });

      return columns;
    },
    isQueued(record) {
      return record?.status?.includes("queued");
    },
    isProcessingCompleted(record) {
      let isCompleted =
        (record?.status == CONST.MODEL_STATUS.COMPLETED.label ||
          this.didCompleteRemeshing(record)) &&
        this.hasStartedProcessingConfigId !== record.id &&
        this.currentStep === 1 &&
        !this.shouldExtractImagesAgain;

      return isCompleted;
    },
    isProcessing(record) {
      return (
        [CONST.MODEL_STATUS.PROCESSING.label].includes(record?.status) ||
        this.hasStartedProcessingConfigId === record.id ||
        this.isRemeshing(record)
      );
    },
    isRemeshing(record) {
      return record?.status == CONST.MODEL_STATUS.REMESHING.label;
    },
    didCompleteRemeshing(record) {
      return record?.status == CONST.MODEL_STATUS.REMESHED.label;
    },
    steps(record) {
      return record?.steps ?? [];
    },
    getButtonTitle(record) {
      return this.isQueued(record)
        ? "Queued"
        : this.isProcessing(record) && this.shouldExtractImages
        ? "Extracting images"
        : this.isProcessing(record) && this.shouldExtractPoses
        ? "Extracting poses"
        : this.isRemeshing(record)
        ? "Remeshing"
        : this.isProcessing(record)
        ? "Processing"
        : this.isProcessingCompleted(record)
        ? "View 3D model"
        : this.type === "video" && !this.didExtractImages
        ? !this.shouldExtractImagesAgain
          ? "Extract images"
          : "Re-extract images"
        : this.currentStep == 0 && !this.didExtractPoses
        ? "Extract poses"
        : this.currentStep == 0 && this.didExtractPoses
        ? "Re-extract poses"
        : "Process";
    },
    async handleRemoveBackground() {
      if (!this.shouldRemoveBackgroundBeChecked) {
        try {
          this.isRemovingBackground = true;
          if (!this.didRemoveBackground)
            this.estimatedTime = await this.getEstimatedTime(this.modelId);
          if (this.estimatedTime !== "00:00") {
            this.estimatedTime = this.$moment(this.estimatedTime, "mm:ss").diff(
              this.$moment().startOf("day"),
              "seconds"
            );
            this.countDown();

            await this.removeBackground(this.modelId);
            clearInterval(this.timer);
            this.estimatedTime = "00:00";
          }
          if (
            (this.currentStep == 0 ||
              this.overiddenRemovedBackground === undefined) &&
            this.type !== "3dImage"
          ) {
            await this.updateBackgroundRemovedStatus();
            this.$notification.success({
              message: "Success",
              description: "The background was removed successfully.",
            });
            this.refreshModelStatus(true);
          }

          if (
            this.overiddenRemovedBackground === false ||
            this.currentStep == 1
          )
            this.overiddenRemovedBackground = true;
        } catch (error) {
          this.$notification.error({
            message: "Error",
            description: error.response.data.message,
          });
          this.refreshModelStatus(true);
        } finally {
          this.isRemovingBackground = false;
          this.estimatedTime = "00:00";
        }
      } else {
        this.isRemovingBackground = true;
        if (this.currentStep == 0) {
          await this.updateBackgroundRemovedStatus();
          this.refreshModelStatus(true);
        }
        this.overiddenRemovedBackground = false;
        this.isRemovingBackground = false;
      }
    },
    countDown() {
      this.timer = setInterval(() => {
        this.estimatedTime--;
        if (this.estimatedTime <= 0) {
          clearInterval(this.timer);
          this.estimatedTime = "00:00";
        }
      }, 1000);
    },
    async updateBackgroundRemovedStatus() {
      let config = this.model?.trainingParams?.find((config) =>
        [true, false].includes(
          config.parameter_json_data?.common?.did_extract_poses
        )
      );
      if (!config) config = this.trainingParams[0];

      await this.updateModelParams(config, true, false, false, false, true);
    },
    isDisabled(record) {
      return (
        this.isQueued(record) ||
        this.isProcessing(record) ||
        this.isProcessingCompleted(record)
      );
    },
    handleAddConfig() {
      // add a new config to trainingParams array
      this.$set(this.form, "new", {});
      this.setDefaultParams({ id: "new" });
      this.setCurrentModel({
        ...this.model,
        trainingParams: [
          ...this.model.trainingParams,
          {
            id: "new",
            model_id: this.modelId,
            status: "uploaded",
            steps: [],
            parameter_json_data: {},
          },
        ],
      });
    },
    handleEditConfig(record) {
      this.$set(this.form[record.id], "isEditing", true);
    },
    cancelEditConfig(record) {
      this.$set(this.form[record.id], "isEditing", false);
      if (record.id !== "new") this.initParams(true);
    },
    getConfigName(record) {
      let index = this.trainingParams.length;
      return this.shouldExtractImages
        ? "Image extraction"
        : this.currentStep == 0
        ? "Pose estimation"
        : record.id === "new"
        ? `config_${index}`
        : record?.parameter_json_data?.common?.name;
    },
    getStepStatus(status) {
      return status === "Start"
        ? "process"
        : status === "Done"
        ? "finish"
        : "error";
    },
    handleDeleteConfig(record) {
      this.$confirm({
        title: "Are you sure you want to delete this config?",
        content: "This action cannot be undone.",
        okText: "Yes",
        okType: "danger",
        cancelText: "No",
        centered: true,
        onOk: async () => {
          try {
            if (record.id === "new") {
              this.setCurrentModel({
                ...this.model,
                trainingParams: this.trainingParams.filter(
                  (config) => config.id !== record.id
                ),
                forceDeleteConfig: true,
              });
            } else {
              await this.deleteConfig(record.id);
              this.refreshModelStatus();
            }
            this.$notification.success({
              message: "Success",
              description: "The config was deleted successfully.",
            });
            this.refreshModelStatus();
          } catch (error) {
            this.$notification.error({
              message: "Error",
              description: error.response.data.message,
            });
          }
        },
      });
    },
    handleExtractImagesAgain() {
      this.shouldExtractImagesAgain = true;
      this.showPreviewModal = false;
    },
    beforeUpload(file) {
      this.fileList = [file];
      return false;
    },
    handleRemove(file) {
      this.fileList = this.fileList.filter((f) => f.uid !== file.uid);
    },
    async handleUpload() {
      let config = this.trainingParams[0];
      let newConfigId = await this.updateModelParams(
        config,
        false,
        false,
        false,
        false,
        true
      );

      const formData = new FormData();
      formData.append("files", this.fileList[0]);
      formData.append("configId", newConfigId ?? config.id);
      this.uploading = true;

      try {
        await this.uploadPoses(formData);
        this.$notification.success({
          message: "Success",
          description: "Uploaded successfully.",
        });
        this.refreshModelStatus();
        this.currentStep = 1;
      } catch (error) {
        this.updateModelParams(
          newConfigId ? { id: newConfigId } : config,
          false,
          false,
          false,
          false,
          true,
          true
        );
        this.$notification.error({
          message: "Error",
          description: error.response.data.message,
        });
        this.currentStep = 0;
      } finally {
        this.uploading = false;
      }
    },
    handleStepChange(step) {
      if (step == 1) return;

      if (this.didUploadPoses) this.shouldUploadPoses = true;
    },
  },
  beforeDestroy() {
    if (this.interval) {
      clearInterval(this.interval);
    }
    this.setCurrentModel(null);
  },
};
</script>

<style>
.processing-container {
  min-height: calc(100vh - 243px);
  display: flex;
  flex-direction: column;
}
.processing-button {
  margin-top: auto;
}
.active {
  color: #1890ff !important;
}
.stage-list-container {
  max-height: calc(100vh - 243px);
  overflow: auto;
}
.image-list-container {
  max-height: calc(100vh - 243px);
  overflow-x: hidden;
  overflow-y: auto;
  text-align: center;
}
@media only screen and (min-height: 769px) {
  .param-form .ant-form-item {
    margin-bottom: 20px;
  }
}

@media only screen and (max-height: 768px) {
  .param-form .ant-form-item {
    margin-bottom: 10px;
  }
}

@media only screen and (min-width: 825px) {
  .param-col {
    max-height: calc(100vh - 243px);
    overflow: auto;
  }
}
.step-name {
  font-weight: bold;
}
.step-description {
  font-size: 12px;
  color: #999;
}
.steps {
  margin-top: 32px;
}

@media only screen and (min-width: 825px) {
  .fixed-width-table table {
    table-layout: fixed;
    width: 100% !important;
  }
}

.outer-table .ant-table-row-expand-icon-cell {
  display: none;
}

.outer-table
  .ant-table-expanded-row.ant-table-expanded-row-level-1
  > td:first-child {
  display: none;
}
</style>