<template>
  <div>
    <a-form
      style="max-width: 500px; margin: 40px auto 0"
      class="upload-container"
    >
      <div class="text-center mb-4">
        <a-radio-group
          v-model="fileType"
          button-style="solid"
          @change="fileList = []"
        >
          <a-radio-button value="video"> Video </a-radio-button>
          <a-radio-button value="image"> Pictures </a-radio-button>
          <a-radio-button value="3dImage">
            Images with camera poses
          </a-radio-button>
        </a-radio-group>
      </div>
      <a-form-item style="text-align: center">
        <a-upload
          :accept="
            fileType === 'image'
              ? 'image/*'
              : fileType === '3dImage'
              ? '.r3d'
              : 'video/*'
          "
          :directory="fileType === 'image'"
          :multiple="fileType === 'image'"
          :file-list="fileList"
          :listType="fileType === 'image' ? 'picture' : 'text'"
          :before-upload="beforeUpload"
          :remove="handleRemove"
        >
          <a-button type="primary" ghost :class="fileList.length ? 'mb-4' : ''">
            <a-icon type="upload" /><span
              v-if="['video', '3dImage'].includes(fileType)"
            >
              Select file</span
            >
            <span v-else> Select directory</span>
          </a-button>
        </a-upload>
      </a-form-item>

      <a-form-item style="text-align: center">
        <a-button
          type="primary"
          @click="handleUpload"
          :loading="isLoading"
          :disabled="!fileList.length"
          >Upload</a-button
        >
      </a-form-item>
    </a-form>
  </div>
</template>

<script>
// all image extensions
const extensions = [
  "jpg",
  "jpeg",
  "png",
  "gif",
  "bmp",
  "tiff",
  "tif",
  "svg",
  "webp",
  "ico",
  "heic",
  "cur",
  "jfif",
  "pjpeg",
  "pjp",
  "avif",
  "apng",
];

import { mapActions } from "vuex";
export default {
  name: "Step2",
  data() {
    return {
      fileList: [],
      fileType: "video",
      isLoading: false,
    };
  },
  methods: {
    ...mapActions(["uploadFiles", "createWorkspace"]),
    beforeUpload(file) {
      let thumbUrl = "";
      if (this.fileType === "image") {
        thumbUrl = URL.createObjectURL(file);
        file.thumbUrl = thumbUrl;
      }

      if (this.fileType === "video") {
        this.fileList = [file];
      } else if (this.fileType === "image") {
        for (const ext of extensions) {
          if (
            file.name.endsWith(ext) ||
            file.name.endsWith(ext.toUpperCase())
          ) {
            this.fileList.push(file);
          }
        }
      } else if (this.fileType === "3dImage") {
        if (file.name.endsWith(".r3d")) {
          this.fileList = [file];
        }
      }
      return false;
    },
    async handleUpload() {
      this.isLoading = true;
      const formData = new FormData();
      this.fileList.forEach((file) => {
        formData.append("files", file);
      });
      formData.append("type", this.fileType);
      let res = await this.uploadFiles(formData);
      let modelId = res?.data?.id?.[0];
      try {
        await this.createWorkspace(modelId);
      } catch (error) {
        console.log(error);
      }
      this.isLoading = false;

      this.$router.push({
        name: `process-id___en`,
        params: { id: modelId, isFromUpload: true },
      });
    },
    handleRemove(file) {
      this.fileList = this.fileList.filter((f) => f.uid !== file.uid);
    },
  },
};
</script>
<style>
.upload-container .ant-upload-list.ant-upload-list-picture {
  max-height: calc(100vh - 400px);
  overflow: auto;
}
</style>