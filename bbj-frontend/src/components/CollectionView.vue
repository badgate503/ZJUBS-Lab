
<template>
  <div class="title" @click="moun">我收藏的商品</div>
  <el-divider></el-divider>
  <div class="content-cont" >
    <div class="panel-cont" v-for="item in favorList">
      <CollectionPanel  :info="item"/>
    </div>
    <div class="empty-cont" v-show="isEmpty">
      <el-empty  description="未收藏任何商品"></el-empty>
    </div>


  </div>



</template>

<script>
import CollectionPanel from "./CollectionPanel.vue";
import axios from "axios";

export default {

  data() {
    return {
      favorList:[],
      isEmpty:false,
    }

  },
  components: {

  },
  methods: {
    removePanel(item){
      this.favorList.splice(this.favorList.indexOf(item),1)
    },

  },

  mounted() {
    this.isEmpty=true
    axios.post("/api/get_keyword_info", {},{
      withCredentials: true,
      headers: {
        "content-type": "application/json",
        'X-CSRFTOKEN': this.$cookies.get("csrftoken")
      }
    }).then(res=>{
      this.favorList = res.data
      console.log(this.favorList)
      this.isEmpty=(this.favorList.length===0)
    })

  }
}
</script>

<style scoped>
.title{
  margin-left: 20px;
  margin-top: 20px;
  font-size: 40px;
}
.content-cont{
  display: flex;
  width: 100%;
  flex-direction: row;
  flex-wrap: wrap;
}
.panel-cont{
  width: 30%;
}
.empty-cont{
  display: flex;
  flex-direction: row;
  width: 100%;
  justify-content: center;
  margin-top: 50px;
}

</style>