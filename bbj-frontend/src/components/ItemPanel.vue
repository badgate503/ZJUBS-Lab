<template>
  <div class="collection-main">

    <el-card  shadow="always"class="coll-container">
      <div class="img-cont">
        <img :src="info.img">
      </div>
      <div class="name-price">
        <div class="name-icon">
          <el-icon size="large"><Discount /></el-icon><div class="item-name">{{ info.name }}</div>
        </div>

      </div>
      <div class="price-cont">
        <div class="price">¥{{parseFloat(info.price).toFixed(2)}}</div>
        <div class="operations">
          <el-button @click="onClick" type="warning">跳转{{info.fromwhich==="taobao"? '淘宝':'京东'}}页面</el-button>
        </div>
      </div>





    </el-card>




  </div>
</template>

<script>
import axios from "axios";
import ECharts from "vue-echarts";
export default {
  data() {
    return {
      tname:""
    }
  },
  props: {
    info:Object,
  },
  mounted() {
    this.tname= (this.info.fromwhich === "jingdong") ? "京东":"淘宝"
  },
  methods: {
    onClick() {
      window.location.href= this.info.link
    }
  },

}
</script>

<style scoped>
.img-cont{
  width: 100%;
}
.img-cont img{
  width: 100%;
}

.coll-container{
  margin-left: 20px;
  margin-top: 20px;
  width: 100%;
}
.switch-tab{
  margin-top: 10px;
}
.item-name{
  font-size: medium;
  margin-left: 10px;
}
.name-price{
  margin-top: 10px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}
.price-cont{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}
.name-icon{
  display: flex;
  flex-direction: row;
  align-items: center;
}
.price{
  margin-top: 10px;
  font-size: x-large;
  color: #cf2020;
}
.item-num{
  font-size: small;
  color: #9a9a9a;
}
.operations{
  margin-top:10px;
}
</style>