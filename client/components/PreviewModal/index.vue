<template>
  <a-modal
    :footer="false"
    visible
    @cancel="$emit('cancel')"
    centered
    :width="1200"
    destroyOnClose
  >
    <a-row slot="title" type="flex" justify="space-between">
      <a-col :span="12">
        {{ modelId }}
      </a-col>
      <a-col v-if="type == 'image'" :span="12" class="text-right">
        <span class="mr-5">
          <a-button
            type="primary"
            icon="unordered-list"
            :ghost="viewMode != 'list'"
            @click="viewMode = 'list'"
          />
          <a-button
            type="primary"
            icon="appstore"
            :ghost="viewMode != 'grid'"
            @click="viewMode = 'grid'"
          />
        </span>
      </a-col>
    </a-row>
    <FileList :files="files" :viewMode="viewMode" :type="type" />

    <div v-if="shouldRenderExtractImagesButton" class="text-center mt-2">
      <a-button type="primary" @click="$emit('extractImages')"
        >Extract images</a-button
      >
    </div>
  </a-modal>
</template>

<script>
import FileList from "@/components/FileList";
export default {
  props: ["files", "modelId", "type", "shouldRenderExtractImagesButton"],
  components: {
    FileList,
  },
  data() {
    return {
      viewMode: "grid",
    };
  },
};
</script>

<style>
.preview-image-grid {
  width: 100%;
  height: 229px;
  object-fit: contain;
}
.preview-image-list {
  max-width: 100%;
  object-fit: contain;
}
.preview-list .ant-card-head {
  font-size: 12px;
}
.preview-list .ant-card-body {
  padding: 8px;
  zoom: 1;
}
</style>
