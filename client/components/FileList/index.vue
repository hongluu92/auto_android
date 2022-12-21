<template>
  <div>
    <a-list
      v-if="type == 'image'"
      class="preview-list"
      :grid="
        viewMode == 'grid'
          ? {
              gutter: 16,
              xs: 1,
              sm: 2,
              md: maxGridColumns,
              lg: maxGridColumns,
              xl: maxGridColumns,
              xxl: maxGridColumns,
            }
          : undefined
      "
      :data-source="files"
    >
      <a-list-item slot="renderItem" slot-scope="item, index">
        <a-card>
          <div slot="title" class="image-title">
            <a-tooltip
              title="Select file for deletion"
              :arrowPointAtCenter="true"
              placement="left"
              :getPopupContainer="(a) => a.parentNode"
            >
              <a-checkbox
                v-if="shouldShowCheckbox"
                :checked="checkIfFileIsSelected(item)"
                @change="(e) => $emit('checkboxChange', e.target.checked, item)"
                class="mr-2"
              />
            </a-tooltip>

            <a-tooltip
              :title="getImageTitle(item)"
              :getPopupContainer="(a) => a.parentNode"
            >
              {{ getImageTitle(item) }}
            </a-tooltip>
          </div>
          <a :href="getImageUrl(item)">
            <img
              :class="{
                'preview-image-grid': viewMode == 'grid',
                'preview-image-list': viewMode == 'list',
              }"
              :src="`${getImageUrl(item)}`"
              alt="No preview available"
            />
          </a>
        </a-card>
      </a-list-item>
    </a-list>

    <video v-else id="video-preview" controls class="fit-video-height">
      <source :src="getVideoUrl()" type="video/mp4" />
    </video>
  </div>
</template>

<script>
export default {
  props: [
    "files",
    "type",
    "viewMode",
    "maxGridCols",
    "shouldShowCheckbox",
    "checkedFiles",
  ],
  computed: {
    maxGridColumns() {
      return this.maxGridCols || 4;
    },
  },
  methods: {
    getImageUrl(image) {
      return `${process.env.API_BASE_URL}${image}`;
    },
    getImageTitle(image) {
      return image.split("/").pop();
    },
    getVideoUrl() {
      return `${process.env.API_BASE_URL}${this.files[0]}`;
    },
    checkIfFileIsSelected(file) {
      let fileName = file.split("/").pop();
      return this.checkedFiles.includes(fileName);
    },
  },
};
</script>

<style>
.fit-video-height {
  max-height: calc(100vh - 233px);
  width: 100%;
}
.image-title {
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
}
</style>