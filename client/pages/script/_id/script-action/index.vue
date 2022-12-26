<template>
  <div>
    <h2> {{ script?.name }}</h2>
    <a-row :gutter="24" type="flex" justify="space-between" align="top" v-if="script && current_img">
      <a-col :md="12" :xs="24" @click.ctrl.exact="onCtrClick()" class="img_layout" style="margin-top: 26px;">
        <span style="margin-right: 20px;">Position : {{ Math.round(curMouse.x) }} {{ Math.round(curMouse.y) }}</span>
        <span>Rect (x,y,w,h): {{ Math.round(curRectImage.x) }} {{ Math.round(curRectImage.y) }} {{
            Math.round(curRectImage.width)
        }} {{ Math.round(curRectImage.height) }}</span>
        <v-stage v-if="current_img" ref="stage" :config="configKonva" @mouseenter="handleMouseEnter('stage')"
          @mousemove="handleMouseMove" @mouseDown="handleMouseDown" @contextmenu="(e) => handleRightClick(e)">
          <v-layer ref="layer">
            <v-image ref="myImg" :config="{
              image: current_img
            }" />
            <v-rect v-if="curRectImage" :key="scriptId + '_image'" :config="curRectImage" @dragend="handleDragEnd" />
            <v-rect v-if="curRectClick" :key="scriptId + '_click'" :config="curRectClick" />
            <v-transformer ref="transformer" />
          </v-layer>
        </v-stage>
        <div style="color: red;">Ctrl + click to remove box</div>
        <div style="visibility: hidden; height: 0.5rem" :id="`stageContainer22`" class="title text-center">
          Input image
        </div>
        <!-- <img class="current-img" :src="current_img" style="height: auto; max-height: 600px !important;" @click="onImgPosition()"/> -->
      </a-col>
      <a-col :md="12" :xs="24">
        <div class="text-right">
          <a-button type="warning" @click="onRunAll(scripAction)">Run all <a-icon type="caret-right" /></a-button>
          <a-button><a-icon type="plus" /> Add </a-button>
        </div>
        <a-row style="margin-top: 10px;max-height: 486px;overflow-y: scroll;">
          <a-card v-for="scripAction, index in scriptActionList" :class="isEditing(scripAction) ? 'active' : ''">
            <div style="position: absolute; left: 20px; top: 10px; z-index: 100; zoom: 60%;">
              <a-badge :count="index + 1" :number-style="{
                backgroundColor: '#fff',
                color: '#999',
                boxShadow: '0 0 0 1px #d9d9d9 inset',
              }" style="margin-right:10px;" />
              <a-radio-group v-model="scripAction.action_type" button-style="solid" @change="onCtrClick()"
                :disabled="!isEditing(scripAction)">
                <a-radio-button :value="CONST.ACTION_TYPE.TAP"> Click </a-radio-button>
                <a-radio-button :value="CONST.ACTION_TYPE.SWIPE"> Swipe </a-radio-button>
                <a-radio-button :value="CONST.ACTION_TYPE.TAP_BY_IMAGE">Click by Image</a-radio-button>
                <a-radio-button :value="CONST.ACTION_TYPE.CHECK_BY_IMAGE">Check by image</a-radio-button>
                <a-radio-button :value="CONST.ACTION_TYPE.KEY_EVENT">Key event</a-radio-button>
              </a-radio-group>
            </div>
            <div style="position: absolute; right: 20px; top: 10px; z-index: 100; zoom: 60%;">
              <a-button type="warning" @click="onRun(scripAction)">Run <a-icon type="caret-right" /></a-button>
              <a-button type="primary" v-if="!isEditing(scripAction)" @click="onEditing(scripAction)"><a-icon
                  type="edit" />
              </a-button>
              <a-button v-if="isEditing(scripAction)" @click="curScriptAction = {}">Cancel </a-button>
              <a-button v-if="isEditing(scripAction)" type="primary" @click="curScriptAction = {} = false"><a-icon
                  type="save" />
                Save</a-button>
            </div>

            <a-form layout="inline" style="zoom: 80%; margin-top: 3px;">
              <!-- Image of Script Action -->
              <a-form-item>
                <v-stage v-if="current_img" ref="stage-in-form-{{ scripAction.id }}" :config="configKonvaToView"
                  class="ant-col ant-form-item-control-wrapper">
                  <v-layer ref="layer">
                    <v-image ref="myImg" :config="{
                      image: current_img
                    }" />
                    <v-rect v-if="curRectImage" :key="scripAction.id + '_image_in_form'" :config="curRectImage" />
                    <v-rect v-if="curRectClick" :key="scripAction.id + '_click_in_form'" :config="curRectClick" />
                    <v-transformer ref="transformer" />
                  </v-layer>
                </v-stage>
              </a-form-item>
              <a-form-item label="Mô tả" layout="inline">
                <input :value="scripAction.description" :disabled="!isEditing(scripAction)" />
              </a-form-item>
              <a-form-item label="Position" layout="inline"
                v-if="scripAction.action_type == CONST.ACTION_TYPE.TAP || scripAction.action_type == CONST.ACTION_TYPE.TAP_BY_IMAGE || scripAction.action_type == CONST.ACTION_TYPE.CHECK_BY_IMAGE">
                <input v-if="scripAction.action_type == CONST.ACTION_TYPE.TAP" :value="scripAction.tap_position"
                  disabled="true" style="width: 65px;;" />
                <input
                  v-if="scripAction.action_type == CONST.ACTION_TYPE.TAP_BY_IMAGE || scripAction.action_type == CONST.ACTION_TYPE.CHECK_BY_IMAGE"
                  :value="scripAction.img_compare_bb" disabled="true" style="width: 112px;;" />
              </a-form-item>
              <a-form-item label="Loop" layout="inline">
                <input :value="scripAction.loop" style="width: 30px;" :disabled="!isEditing(scripAction)" />
              </a-form-item>
              <a-form-item label="Delay" layout="inline">
                <input :value="scripAction.loop" style="width: 50px;" :disabled="!isEditing(scripAction)" />
              </a-form-item>
              <a-form-item label="Key Event" layout="inline"
                v-if="scripAction.action_type == CONST.ACTION_TYPE.KEY_EVENT">
                <input :value="scripAction.key_event" :disabled="!isEditing(scripAction)" />
              </a-form-item>

            </a-form>
          </a-card>
        </a-row>
      </a-col>
    </a-row>
  </div>
</template>
<script>
import { mapState, mapActions, mapMutations } from "vuex";
import * as CONST from "@/constants/index.js";
// import { columns } from "./const";
import modelMixin from "@/mixins/modelMixin";

export default {
  mixins: [modelMixin],
  components: {
  },
  data() {
    return {
      CONST,
      current_img: null,
      stageWidthMax: 500,
      stageHeightMax: 500,
      stageWidth: 1,
      stageHeight: 1,
      imagePath: "",
      isDrawing: false,
      curRectImage: {},
      curRectClick: {},
      curMouse: {
        x: 0,
        y: 0
      },
      curScriptAction: {}
    };
  },
  async created() {
    this.initcurRectImage()
    this.initcurRectClick()
    await this.reload_current_img()
    await this.getScript(this.scriptId);
    await this.getScriptActions(this.scriptId);
    this.imagePath = await this.getImgSrc("current_img.png")
    const image = new window.Image();
    image.src = this.imagePath;
    let max_height = 600
    let max_width = window.innerWidth / 2 - 60
    image.onload = () => {
      let scale = Math.min(max_height / image.height, max_width / image.width)
      image.height = image.height * scale
      image.width = image.width * scale
      this.imageHeight = image.height
      this.imageWidth = image.width
      this.stageWidth = image.width;
      this.stageHeight = image.height;
      this.current_img = image;

    };


  },
  mounted() {
    window.setTimeout(() => {
      this.updateStageWidth();
    })

  },
  computed: {
    ...mapState(["script"]),
    scriptId() {
      return this.$route.params.id;
    },

    type() {
      return this.script?.type;
    },
    imgPosX() {
      return (this.stageWidth / this.minScale - this.imageWidth) / 2;
    },
    imgPosY() {
      return (this.stageHeight / this.minScale - this.imageHeight) / 2;
    },

    minScale() {
      return Math.min(
        this.stageHeightMax / this.imageHeight,
        this.stageWidthMax / this.imageWidth
      );
    },
    configKonva() {
      return {
        width: this.stageWidth,
        height: this.stageHeight,

        // scaleX: 1,
        // scaleY: 1,
      }
    },
    configKonvaToView() {
      return {
        width: this.stageWidth / 9,
        height: this.stageHeight / 9
      }
    },
  },
  methods: {
    ...mapActions(["getScript", "getImgSrc", "reload_current_img", "getScriptActions"
    ]),
    ...mapMutations([
      "scriptActionList"
    ]),

    handleDragEnd(e) {
      const rect = this.curRectImage
      rect.x = e.target.x();
      rect.y = e.target.y();
      this.updateCurScriptActionPosition()
    },
    onImgPosition(e) {

    },
    zoom(e, refName) {
      var scaleBy = 1.1;
      const node = this.$refs[refName].getNode();
      const stage = node.getStage();

      e.evt.preventDefault();

      var oldScale = stage.scaleX();
      var pointer = stage.getPointerPosition();

      var mousePointTo = {
        x: (pointer.x - stage.x()) / oldScale,
        y: (pointer.y - stage.y()) / oldScale,
      };

      let direction = e.evt.deltaY > 0 ? -1 : 1;
      if (e.evt.ctrlKey) {
        direction = -direction;
      }

      var newScale = direction > 0 ? oldScale * scaleBy : oldScale / scaleBy;
      newScale = Math.max(
        refName.indexOf("2") > -1 ? this.minScale2 : this.minScale,
        newScale
      );
      stage.scale({ x: newScale, y: newScale });

      var newPos = {
        x: pointer.x - mousePointTo.x * newScale,
        y: pointer.y - mousePointTo.y * newScale,
      };
      stage.position(newPos);
    },
    handleMouseEnter(refName) {
      const node = this.$refs[refName].getNode();
      const stage = node.getStage();
      stage.container().style.cursor = "grab";

    },
    handleMouseMove() {
      const point = this.$refs.stage.getNode().getRelativePointerPosition();
      if (this.isDrawing) {
        this.curRectImage.width = point.x - this.curRectImage.x;
        this.curRectImage.height = point.y - this.curRectImage.y;
      }
      this.curMouse.x = point.x
      this.curMouse.y = point.y

    },
    handleRightClick(e) {
      e.evt.preventDefault();
    },
    handleMouseDown(e) {
      // update the state
      const isLeft = e.evt.button === 0;
      if (isLeft) {
        this.isDrawing = false
      } else {
        const stage = e.target.getStage();
        const stageLocation = stage.getPointerPosition();
        this.isDrawing = true
        if (this.curScriptAction.action_type) {
          if (this.curScriptAction.action_type == CONST.ACTION_TYPE.TAP) {
            this.curRectClick.x = stageLocation.x;
            this.curRectClick.y = stageLocation.y;
            this.curRectClick.width = 10;
            this.curRectClick.height = 10;
            console.log(this.curRectClick)
          } else {
            this.curRectImage.x = stageLocation.x;
            this.curRectImage.y = stageLocation.y;
            this.curRectImage.width = 0
            this.curRectImage.height = 0
            this.curRectImage.rotation = e.target.rotation();
            this.curRectImage.scaleX = e.target.scaleX();
            this.curRectImage.scaleY = e.target.scaleY();
          }
        }
      }
      this.updateCurScriptActionPosition()
      // change fill
    },
    updateTransformer() {
      // here we need to manually attach or detach Transformer node
      const transformerNode = this.$refs.transformer.getNode();
      const stage = transformerNode.getStage();
      const { selectedShapeName } = this;

      const selectedNode = stage.findOne('.' + selectedShapeName);
      // do nothing if selected node is already attached
      if (selectedNode === transformerNode.node()) {
        return;
      }

      if (selectedNode) {
        // attach to another node
        transformerNode.nodes([selectedNode]);
      } else {
        // remove transformer
        transformerNode.nodes([]);
      }
    },
    initcurRectImage() {
      this.curRectImage = {
        rotation: 0,
        x: 0,
        y: 0,
        width: 0,
        height: 0,
        scaleX: 0,
        scaleY: 0,
        stroke: 'red',
        name: 'rect_img',
        draggable: true,
      }
    },
    initcurRectClick() {
      this.curRectClick = {
        x: 0,
        y: 0,
        width: 0,
        height: 0,
        fill: 'red',
        cornerRadius: 15
      }
    },
    onEditing(scripAction) {
      this.curScriptAction = scripAction
    },
    isEditing(scripAction) {
      return this.curScriptAction.id == scripAction.id
    },
    onRun(scripAction) {

    },
    onRunAll(scripAction) {

    },
    onCtrClick() {
      this.initcurRectImage()
      this.initcurRectClick()
    },
    updateCurScriptActionPosition() {
      if (this.curScriptAction.action_type == CONST.ACTION_TYPE.TAP) {
        this.curScriptAction.tap_position = `${Math.round(this.curRectClick.x)} ${Math.round(this.curRectClick.y)}`
      }
      if (this.curScriptAction.action_type == CONST.ACTION_TYPE.TAP_BY_IMAGE || this.curScriptAction.action_type == CONST.ACTION_TYPE.CHECK_BY_IMAGE) {
        this.curScriptAction.img_compare_bb = `${Math.round(this.curRectImage.x)} ${Math.round(this.curRectImage.y)} ${Math.round(this.curRectImage.width)} ${Math.round(this.curRectImage.height)}`
      }
    },

  },
  beforeDestroy() {

  },
  async mounted() {

  }
};
</script>

<style>
.ant-card {
  margin-top: 5px;
}

.current-img {
  border: solid 1px gray;
}

.ant-form-item {
  margin-bottom: 5px;
}

.ant-form-item input {
  height: 26px;
  width: fit-content;
}

.ant-card-body {
  padding: 26px 5px 5px 9px;
}

.active {
  border: solid red 1px;
}

.img_layout {
  margin-top: 26px;
}
</style>