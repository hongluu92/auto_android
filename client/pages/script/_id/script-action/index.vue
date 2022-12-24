<template>
  <div>
    <h2 > {{ script?.name }}</h2>
    <a-row :gutter="24" type="flex" justify="space-between" align="top" v-if="script && current_img ">
        <a-col :md="12" :xs="24"  >
          <v-stage 
            v-if ="current_img"
            ref="stage" 
            :config="configKonva"
            @mouseenter="handleMouseEnter('stage')"
            @mousemove="handleMouseMove"
            @mouseDown="handleMouseDown"
            @contextmenu="(e) => handleRightClick(e)"
          >
            <v-layer ref="layer">
              <v-image
                ref="myImg"
                :config="{
                  image: current_img
                }"
              />
              <v-rect
                v-if="curRec"
                :key="scriptId"
                :config="curRec"
                @transformend="handleTransformEnd"
              />
              <v-transformer ref="transformer" />
            </v-layer>
          </v-stage>
          <div
            style="visibility: hidden; height: 0.5rem"
            :id="`stageContainer22`"
            class="title text-center"
          >
            Input image
          </div>
          <!-- <img class="current-img" :src="current_img" style="height: auto; max-height: 600px !important;" @click="onImgPosition()"/> -->
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
      stageWidthMax:700,
      stageHeightMax:600,
      stageWidth: 1,
      stageHeight: 1,
      imagePath: "", 
      isEditing: true,
      isDrawing: false,
      curRec:{
          rotation: 0,
          x: 0,
          y: 0,
          width: 0,
          height: 0,
          scaleX: 0,
          scaleY: 0,
          stroke: 'red',
          name: 'rect1',
          draggable: true,
      }
    };
  },
  async created(){
    await this.reload_current_img()
    await this.getScript(this.scriptId);
    this.imagePath = await this.getImgSrc("current_img.png")
    const image = new window.Image();
    image.src = this.imagePath;
    let max_height = 500
    let max_width = 800
    image.onload = () => {
      let scale = Math.min(max_height/image.height , max_width/image.width )
      image.height = image.height*scale
      image.width = image.width*scale
      this.imageHeight = image.height
      this.imageWidth = image.width
      this.stageWidth = image.width;
      this.stageHeight = image.height;
      this.current_img = image;
    };
    
    
  },
  mounted(){
    window.setTimeout(()=>{
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
  },
  methods: {
    ...mapActions(["getScript", "getImgSrc","reload_current_img"
    ]),
    ...mapMutations([

    ]),
    handleTransformEnd(e){
      const rect = this.rectangles.find(
        (r) => r.name === this.selectedShapeName
      );
      // update the state
      rect.x = e.target.x();
      rect.y = e.target.y();
      rect.rotation = e.target.rotation();
      rect.scaleX = e.target.scaleX();
      rect.scaleY = e.target.scaleY();
    },
    onImgPosition(e){

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
      console.log(refName)
      const node = this.$refs[refName].getNode();
      const stage = node.getStage();
      stage.container().style.cursor = "grab";
      
    },
    handleMouseMove() {
      if (this.isDrawing){
        const point = this.$refs.stage.getNode().getRelativePointerPosition();
        this.curRec.width = point.x - this.curRec.x;
        this.curRec.height = point.y - this.curRec.y;
      }
        
    },
    handleRightClick(e) {
      e.evt.preventDefault();
    },
    handleMouseDown(e) {
      // update the state
      const isLeft = e.evt.button === 0;
      if(isLeft) {
        this.isDrawing = false
        console.log(this.curRec)
      }else{
          const stage = e.target.getStage();
          const stageLocation = stage.getPointerPosition();
          this.isDrawing = true
          this.curRec.x = stageLocation.x;
          this.curRec.y = stageLocation.y;
          this.curRec.width = 0
          this.curRec.height = 0
          this.curRec.rotation = e.target.rotation();
          this.curRec.scaleX = e.target.scaleX();
          this.curRec.scaleY = e.target.scaleY();
      }
      
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
    
  },
  beforeDestroy() {
    
  },
  async mounted() {
   
  }
};
</script>

<style>
.current-img {
  border: solid 1px gray;
}
</style>