<script>
import axios from "axios";
import FrontView from "./FrontView.vue";

export default {
  data() {
    return{
      Title:"",
      Items:[]
    }

  },
  props: {
    info:Object,
    fatherMethod:Function,
  },
  methods: {
  },

}
</script>

<template>
  <div class="list-cont">
    <div class="center-title">
      <el-text class="item-title" size="large">{{info.title}}</el-text>
      <el-icon style="margin-left: 3px;"><ArrowRight /></el-icon>
    </div>

  <div class="list-item" v-for="item in info.list">
    <el-link type="primary" @click="this.fatherMethod(item)">{{item}}</el-link>
  </div>
  </div>
</template>

<style scoped>
.item-title{
  font-size: 17px;
  color: #000000;
  font-weight: bolder;
}
.center-title{
  display: flex;
  flex-direction: row;
  align-items: center;
}
.list-cont{
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  width: 70%;
  margin-top: 20px;
}
.list-item{
  margin-left: 10px;
}
</style>