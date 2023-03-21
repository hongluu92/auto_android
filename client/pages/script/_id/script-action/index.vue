<template>
  <div>
    <h2> {{ script?.name }}</h2>
    <a-row :gutter="24" type="flex" justify="space-between" align="top" v-if="script && current_img">

      <a-col :lg=12 :md="12" :xs="24" @click.ctrl.exact="onCtrClick()" class="img_layout">
        <span><button type="primary" @click="reloadCurrentImage()"><a-icon type="sync" /> Sync</button></span>
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
      <a-col :lg=12 :md="12" :xs="24">
        <div class="text-right">
          <a-button type="warning" @click="onRunAll(scripAction)">Run all <a-icon type="caret-right" /></a-button>
          <a-button @click="initNewAction()"><a-icon type="plus" /> Add </a-button>
        </div>
        <a-row style="margin-top: 10px;max-height: 486px;overflow-y: scroll;">
          <a-card v-for="scripAction, index in actionList" :class="isEditing(scripAction) ? 'active' : ''"
            v-bind:key="index">
            <div style="margin-bottom: 2px;">
              <a-badge :count="index + 1" :number-style="{
  backgroundColor: '#fff',
  color: '#999',
  boxShadow: '0 0 0 1px #d9d9d9 inset',
}" style="margin-right:10px;" />

            </div>
            <div style="position: absolute; right: 20px; top: 10px; z-index: 100; zoom: 70%;">
              <a-button type="warning" @click="onRun(scripAction)">Run <a-icon type="caret-right" /></a-button>
              <a-button type="primary" v-if="!isEditing(scripAction)" @click="onEditing(scripAction)"><a-icon
                  type="edit" />
              </a-button>
              <a-button v-if="isEditing(scripAction)" type="primary" @click="saveScripAction(scripAction)"><a-icon
                  type="save" />
                Save</a-button>
              <a-button type="danger" @click="deleteScripAction(scripAction)"><a-icon type="delete" />
              </a-button>
              <a-button  @click="addBelow(scripAction, index)"><a-icon type="plus" /> Add below
              </a-button>
            </div>
            <div>
              <a-col :md=8 :xs="24">
                <!-- Image of Script Action -->
                <a-popover placement="left">
                  <template #content>
                    <v-stage v-if="current_img" ref="stage-in-form-{{ scripAction.id }}" :config="configKonvaTooltip"
                      class="ant-col ant-form-item-control-wrapper">
                      <v-layer ref="layer">
                        <v-image ref="myImg" :config="{
  image: scripAction.image_data
}" />
                        <v-rect :key="scripAction.id + '_image_in_form'" :config="getRectImageBy(scripAction)" />
                        <v-rect :key="scripAction.id + '_click_in_form'" :config="getRectClickBy(scripAction)" />
                        <v-transformer ref="transformer" />
                      </v-layer>

                    </v-stage>
                  </template>
                  <v-stage v-if="current_img" ref="stage-in-form-{{ scripAction.id }}" :config="configKonvaToView"
                    class="ant-col ant-form-item-control-wrapper">
                    <v-layer ref="layer">
                      <v-image ref="myImg" :config="{
  image: scripAction.image_data
}" />
                      <v-rect :key="scripAction.id + '_image_in_form'" :config="getRectImageBy(scripAction)" />
                      <v-rect :key="scripAction.id + '_click_in_form'" :config="getRectClickBy(scripAction)" />
                      <v-transformer ref="transformer" />
                    </v-layer>

                  </v-stage>
                </a-popover>
              </a-col>
              <a-col :md=16 :xs="24">
                <a-form layout="inline" style="zoom: 70%; margin-top: 9px;">
                  <a-form-item>
                    <a-radio-group v-model="scripAction.action_type" button-style="solid" @change="onCtrClick()"
                      :disabled="!isEditing(scripAction)">
                      <a-radio-button :value="CONST.ACTION_TYPE.TAP"> Click </a-radio-button>
                      <a-radio-button :value="CONST.ACTION_TYPE.SWIPE"> Swipe </a-radio-button>
                      <a-radio-button :value="CONST.ACTION_TYPE.TAP_BY_IMAGE">Image Click</a-radio-button>
                      <a-radio-button :value="CONST.ACTION_TYPE.CHECK_BY_IMAGE">Image Check</a-radio-button>
                      <a-radio-button :value="CONST.ACTION_TYPE.KEY_EVENT">Key</a-radio-button>
                    </a-radio-group>
                  </a-form-item>

                  <a-form-item label="Mô tả">
                    <input v-model="scripAction.description" :disabled="!isEditing(scripAction)" />
                  </a-form-item>
                  <a-form-item label="Position" layout="inline"
                    v-if="scripAction.action_type == CONST.ACTION_TYPE.TAP || scripAction.action_type == CONST.ACTION_TYPE.TAP_BY_IMAGE || scripAction.action_type == CONST.ACTION_TYPE.CHECK_BY_IMAGE">
                    <input v-if="scripAction.action_type == CONST.ACTION_TYPE.TAP" :value="scripAction.tap_position"
                      disabled="true" style="width: 65px;;" />
                    <input
                      v-if="scripAction.action_type == CONST.ACTION_TYPE.TAP_BY_IMAGE || scripAction.action_type == CONST.ACTION_TYPE.CHECK_BY_IMAGE"
                      v-model="scripAction.img_compare_bb" disabled="true" style="width: 112px;;" />
                  </a-form-item>
                  <a-form-item label="Loop" layout="inline">
                    <input v-model="scripAction.loop" style="width: 30px;" :disabled="!isEditing(scripAction)" />
                  </a-form-item>
                  <a-form-item label="Delay" layout="inline">
                    <input v-model="scripAction.loop" style="width: 50px;" :disabled="!isEditing(scripAction)" />
                  </a-form-item>
                  <a-form-item label="Key Event" layout="inline"
                    v-if="scripAction.action_type == CONST.ACTION_TYPE.KEY_EVENT">
                    <input v-model="scripAction.key_event" :disabled="!isEditing(scripAction)" />
                  </a-form-item>
                </a-form>
              </a-col>
            </div>
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
      scale: 0,
      curAction: {},
      actionList: []
    };
  },
  async created() {
    this.initcurRectImage()
    this.initcurRectClick()
    await this.reload_current_img()
    await this.getScript(this.scriptId);
    this.actionList = await this.getActions(this.scriptId);
    this.actionList.forEach(async action => {
      let image = new window.Image();
      image.src = await this.getImgSrc(action.img);
      image.onload = () => {

        action.image_data = image
      }
    })
    let imagePath = await this.getImgSrc("current_img.png")
    let max_height = 500
    let max_width = window.innerWidth / 2 - 60
    this.loadImage(imagePath, max_height, max_width)
  },
  async mounted() {
    await this.$nextTick()
    debugger
  },
  watch: {
    curAction() {
      this.initcurRectClick()
      this.initcurRectImage()
      this.curAction.scale = this.scale
      setTimeout(() => {
        document.querySelector(".active input").focus()
      })
    },
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
        scaleX: (1 / 4) * this.scale,
        scaleY: (1 / 4) * this.scale,
        width: this.stageWidth / 4,
        height: this.stageHeight / 4
      }
    },
    configKonvaTooltip(){
      return {
        scaleX: (2 / 3) * this.scale,
        scaleY: (2 / 3) * this.scale,
        width: this.stageWidth / 1.5,
        height: this.stageHeight / 1.5
      }
    },
  },
  methods: {
    ...mapActions(["getScript", "getImgSrc", "reload_current_img", "getActions", "updateAction", "createAction", "runAction"
    ]),
    ...mapMutations([
    ]),

    handleDragEnd(e) {
      const rect = this.curRectImage
      rect.x = e.target.x();
      rect.y = e.target.y();
      this.updateCurActionPosition()
    },
    onImgPosition(e) {

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
        if (this.curAction.action_type) {
          if (this.curAction.action_type == CONST.ACTION_TYPE.TAP) {
            this.curRectClick.x = stageLocation.x;
            this.curRectClick.y = stageLocation.y;
            this.curRectClick.width = 10;
            this.curRectClick.height = 10;
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
      this.updateCurActionPosition()
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
    getRectImageBy(action) {
      if (action.action_type == CONST.ACTION_TYPE.TAP_BY_IMAGE || action.action_type == CONST.ACTION_TYPE.CHECK_BY_IMAGE) {
        if (!action.img_compare_bb) return {}
        let pos = action.img_compare_bb.split(" ")
        return {
          x: pos[0]/this.scale,
          y: pos[1]/this.scale,
          width: pos[2]/this.scale,
          height: pos[3]/this.scale,
          stroke: 'red',
        }
      }
      return {}

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
    getRectClickBy(action) {
      if (action.action_type == CONST.ACTION_TYPE.TAP) {
        if (!action.tap_position) return {}
        let pos = action.tap_position.split(" ")
        return {
          x: pos[0]/this.scale,
          y: pos[1]/this.scale,
          width: 20,
          height: 20,
          fill: 'red',
          cornerRadius: 15
        }
      }
      return {}

    },
    initAction() {
      return {
        "action_type": "tap",
        "event_type": null,
        "tap_position": null,
        "swipe_position": null,
        "img_compare_bb": null,
        "key_event": null,
        "img": null,
        "loop": 1,
        "loop_delay": 1000,
        "description": null,
        "script_id": this.scriptId,
        "order_index": 0,
        "parrent_id": null,
        "new_thread": false
      }
    },
    initNewAction() {
      let action = this.initAction()
      this.curAction = action
      if (this.actionList[this.actionList.length - 1])
        action.order_index = this.actionList[this.actionList.length - 1].order_index + 100
      else action.order_index = 1
      this.actionList.push(action)
    },
    addBelow(action, index){
      action = this.initAction()
      this.curAction = action
      this.actionList.splice(index+1, 0, action);
    },
    saveScripAction(action) {
      if (!action.id) {
        this.curAction = this.createAction(action)
      } else {
        this.curAction = this.updateAction(action)
      }
    },
    deleteScripAction(action) {
      if (action.id) {
        this.curAction = this.createAction(action.id)
      }
      this.curAction = {}
      this.actionList = this.actionList.filter(function (item) {
        return item.id != undefined && action.id != item.id
      })
    },
    onEditing(scripAction) {
      this.curAction = scripAction
    },
    isEditing(scripAction) {
      return this.curAction.id == scripAction.id
    },
    async reloadCurrentImage() {
      await this.reload_current_img()
      let imagePath = await this.getImgSrc(`current_img.png?random=${new Date().getTime()}`)
      let max_height = 500
      let max_width = window.innerWidth / 2 - 60
      this.loadImage(imagePath, max_height, max_width)
    },
    async onRun(scripAction) {
      await this.runAction(scripAction)
      this.reloadCurrentImage()
    },
    timeout(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    },
    async onRunAll(scripAction) {
      this.actionList 
    },
    onCtrClick() {
      this.initcurRectImage()
      this.initcurRectClick()
    },
    updateCurActionPosition() {
      if (this.curAction.action_type == CONST.ACTION_TYPE.TAP) {
        this.curAction.tap_position = `${Math.round(this.curRectClick.x)} ${Math.round(this.curRectClick.y)}`
      }
      if (this.curAction.action_type == CONST.ACTION_TYPE.TAP_BY_IMAGE || this.curAction.action_type == CONST.ACTION_TYPE.CHECK_BY_IMAGE) {
        this.curAction.img_compare_bb = `${Math.round(this.curRectImage.x)} ${Math.round(this.curRectImage.y)} ${Math.round(this.curRectImage.width)} ${Math.round(this.curRectImage.height)}`
      }
    },

    loadImage(imagePath, max_height, max_width) {
      const image = new window.Image();
      image.src = imagePath;
      image.onload = () => {
        this.scale = Math.min(max_height / image.height, max_width / image.width)
        image.height = image.height * this.scale
        image.width = image.width * this.scale
        this.imageHeight = image.height
        this.imageWidth = image.width

        this.stageWidth = image.width;
        this.stageHeight = image.height;
        this.current_img = image;
      };
    }

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
  border: solid 1px black;
}

.ant-form-item {
  margin-bottom: 5px;
}

.ant-form-item input {
  height: 26px;
  width: fit-content;
}

.ant-card-body {
  padding: 5px 5px 5px 9px;
}

.active {
  border: solid red 1px;
}

button {
  cursor: pointer;
}

.img_layout {
  margin-top: 25px;
}
</style>