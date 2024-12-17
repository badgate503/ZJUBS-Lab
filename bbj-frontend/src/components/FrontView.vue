<script setup>
import ItemPanel from "./ItemPanel.vue";
import ItemList from "./ItemList.vue";
</script>

<template>
  <div class="front">
    <div class="ret-btn-cont" v-show="!logoShow" @click="onAbortSearch">
      <div class="ret-btn" ><ElIcon size="40px"><Back/></ElIcon></div>
    </div>
    <div class="logo-search">
      <el-collapse-transition>
        <img  v-show="logoShow" class="logo-img" alt="logo" src="../assets/logo_txt.svg"></img>
      </el-collapse-transition>

      <div class="search-bar" v-show="searchNotSubmit">

        <div class="search-bar-cont">

          <el-input
              class="search-bar-bar"
              @click="onSearch"
              v-model="searchQuery"
              size="large"
              clearable
              placeholder="搜一搜"
          />
          <el-button @click="onSearchSubmit(false)" class="search-btn" size="large" type="primary"><el-icon size="large"><Search/></el-icon></el-button>

        </div>

      </div>

    </div>
    <el-collapse-transition>
    <div class="control-group" v-show="!searchNotSubmit && searchHasResult">
    <div class="control-box">
      <a class="title-text">"{{searchQuery}}"的搜索结果</a>
    </div>


    <div class="control-box">
      <div class="info-cont">
        <el-text size="large">淘宝平均价格</el-text>
        <a class="info-price-text">¥{{parseFloat(QueryResInfo.TBavgPrice).toFixed(2)}}</a>
      </div>
      <div class="info-cont">
        <el-text size="large">京东平均价格</el-text>
        <a class="info-price-text">¥{{parseFloat(QueryResInfo.JDavgPrice).toFixed(2)}}</a>
      </div>
      <div class="info-cont">
        <el-text size="large">最低价格</el-text>
        <a class="info-price-text">¥{{parseFloat(QueryResInfo.minPrice).toFixed(2)}}</a>
      </div>
      <div class="info-cont">
        <el-text size="large">最高价格</el-text>
        <a class="info-price-text">¥{{parseFloat(QueryResInfo.maxPrice).toFixed(2)}}</a>
      </div>
    </div>
      <div class="control-box">
      <div class="info-cont">
        <el-text>获取淘宝商品{{QueryResInfo.TBcount}}项; 京东商品{{QueryResInfo.JDcount}}项; 搜索结果更新时间:{{QueryResInfo.updateTime}}</el-text>
      </div>
      </div>
    <div class="control-box-1">

      <div class="control-btn-box">
        <el-button type="primary" @click="onSearchSubmit(true)">重新搜索</el-button>
      </div>
      <div class="control-btn-box">
        <el-button type="primary" @click="onFavorKeyword"><ElIcon style="margin-right: 5px;"><Star/></ElIcon>收藏关键词</el-button>
      </div>
    </div>
      <div class="control-box">
        <div class="swi-cont">
          <el-text size="large">价格升序</el-text>
          <el-switch style="margin-left: 10px;" v-model="price_asc" @change="onSort"/>
        </div>
        <div class="swi-cont">
          <el-text size="large">显示淘宝结果</el-text>
          <el-switch style="margin-left: 10px;" v-model="showTBRes" @change="onSort"/>
        </div>
        <div class="swi-cont">
          <el-text size="large">显示京东结果</el-text>
          <el-switch style="margin-left: 10px;" v-model="showJDRes" @change="onSort"/>
        </div>

      </div>
    </div>
    </el-collapse-transition>
    <el-divider class="el-div-d"></el-divider>
    <transition name="el-fade-in">
      <div v-show="!logoShow">

        <el-empty v-show="searchNotSubmit" description="请输入想找的东西" />
        <el-empty v-show="!loading && (!searchHasResult || (!searchNotSubmit && showResultList.length===0))" description="未找到任何商品" />

        <div v-loading="loading"  class="item-list">
          <div class="item-container" v-for="item in showResultList">
            <ItemPanel :info="item"></ItemPanel>
          </div>
        </div>

      </div>

    </transition>

    <div v-show="logoShow" class="lists-cont" v-for="item in ItemLists">
      <ItemList :info="item" :fatherMethod="onClickItem" ></ItemList>
    </div>

  </div>
</template>

<script>
import axios from "axios";
import ItemPanel from "./ItemPanel.vue";
import {getCurrentUser} from "../utils.js";
import { Search } from '@element-plus/icons-vue'
import 'animate.css'
import ItemList from "./ItemList.vue";
import {ElMessage} from "element-plus";
export default {
  data() {
    return{
      logoShow:true,
      searchQuery:"",
      searchNotSubmit:true,
      searchHasResult:true,
      loading:false,
      qr_src:"",
      price_asc:false,
      searchResult:[],
      showResultList:[],
      showTBRes:true,
      showJDRes:true,
      ItemLists:[
          {
        title:"电脑整机",
        list:["笔记本电脑","游戏本","平板电脑","DIY电脑","服务器/工作站","一体机","闺蜜机","有限自动机","下推自动机","图灵机", "线性有界自动机"]
      },{
        title:"电脑配件",
        list:["显示器","CPU","主板","显卡","硬盘","内存","机箱","电源","散热","显示器","支架","光驱","声卡","装机配件","SSD固态硬盘","组装电脑","USB分线器","鼠标","键盘","网络仪表仪器","U盘","移动硬盘","摄像头","手写板","UPS电源","平板电脑配件","笔记本配件","投屏器","扩展坞"]
      },{
        title:"家具",
        list:["床","床垫","沙发","茶几","电视柜","休闲椅","书架","鞋柜","餐桌","餐椅","餐边柜","酒柜","厨房","衣柜","梳妆台","穿衣镜","水槽","龙头","淋浴花洒","马桶","智能马桶","智能马桶盖","厨卫挂件","浴室柜","浴霸"]
      },{
        title:"流行服饰",
        list:["当季热卖","新品推荐","商场同款","连衣裙","T恤","衬衫","外套","针织衫","风衣","西服","卫衣","马夹","大衣","皮衣/皮草","毛衣","羽绒服","休闲裤","牛仔裤","短裤","直筒裤","工装裤","西裤","运动裤","半身裙"]
      },{
        title:"办公耗材",
        list:["投影机","打印机","传真设备","碎纸机","考勤门禁","收银机","保险柜","安防监控","订书机","票夹","大头针","美工刀","胶带","复写纸","号码机","印泥","账本","计算器"]
      },{
        title:"手机数码",
        list:["新品手机","手机维修","AI手机","5G手机","游戏手机","学习手机","对讲机","手机壳","贴膜","手机存储卡","数据线","充电器","创意配件","手机饰品","手机支架","数码相机","微单相机","单反相机","拍立得","运动相机","胶卷相机","摄像机镜头"]
      },{
        title:"新鲜食品",
        list:["饼干","蛋糕","糖/巧克力","方便食品","肉干","肉脯","营养零食","休闲零食","坚果炒货","蜜饯","果干","苹果","橙子","奇异果/猕猴桃","火龙果","榴莲","芒果","椰子","车厘子","百香果","柚子","国产水果","进口水果","猪肉","牛肉","羊肉","鸡肉","鸭肉","冷鲜肉","内脏类","冷藏熟食","牛排","牛腩","鸡翅"]
      },{
        title:"体育用品",
        list:["乒乓球","羽毛球","篮球","足球","轮滑","滑板","网球","高尔夫","台球","排球","田径鞋"]
      }],
      QueryResInfo:{
        TBavgPrice:0,
        JDavgPrice:0,
        minPrice:0,
        maxPrice:0,
        TBcount:0,
        JDcount:0,
        updateTime:""
      }
    }

  },components: {
    ItemList
  },
  methods: {
    onSearch(){
      this.logoShow = false;
      this.searchHasResult = true;
    },
    onAbortSearch(){
      this.logoShow = true;
      this.loading=false;
      this.searchQuery=''
      this.searchNotSubmit = true;
      this.resetSearchResult()
    },
    resetSearchResult(){
      this.searchHasResult = false;
      this.searchResult = [];
      this.showResultList=[];
      this.showTBRes=true;
      this.showJDRes=true
      this.price_asc=false
    },
    onClickItem(itemname){
      console.log(itemname)
      this.onSearch()
      this.searchQuery=itemname
      this.onSearchSubmit(false)
    },
    onSearchSubmit(forceUpdate){
      this.resetSearchResult()
      this.loading = true
      this.searchNotSubmit = false
      this.searchHasResult = false
      if(this.searchQuery.length === 0 || this.searchQuery === ""){
        ElMessage.error("请输入搜索内容")
        return;
      }
      axios.post("/api/fetchItem",{
        query_name:this.searchQuery,
        forceUpdate:forceUpdate,
      },{
        withCredentials: true,
        headers: {
          "content-type": "application/json",
          'X-CSRFTOKEN': this.$cookies.get("csrftoken")
        }
      }).then(res=>{
        console.log(res.data)
        if(res.data.state === "notlogin") {
          this.loading = false
          ElMessage("请登录淘宝和京东")
          return;
        }
        this.searchResult=res.data.qRes
        this.showResultList = this.searchResult
        this.onSort()

        if(!res.data.keyInfo.hasOwnProperty('update_time'))
          this.QueryResInfo.updateTime = "刚刚"
        else
          this.QueryResInfo.updateTime = res.data.keyInfo.update_time
        this.QueryResInfo.maxPrice = res.data.keyInfo.maxPrice/100
        this.QueryResInfo.minPrice = res.data.keyInfo.minPrice/100
        this.QueryResInfo.TBavgPrice = res.data.keyInfo.TBavgPrice/100
        this.QueryResInfo.JDavgPrice = res.data.keyInfo.JDavgPrice/100
        this.QueryResInfo.JDcount = res.data.keyInfo.JDcount
        this.QueryResInfo.TBcount = res.data.keyInfo.TBcount
        this.searchNotSubmit = false;
        if(res.data.qRes !== null && res.data.qRes.length !== 0) {
          this.searchHasResult = true;
        }
        this.loading = false
      }).catch(e=>{
        console.log(e)
        this.searchHasResult = false;
        this.loading = false;
        ElMessage.error("出现内部错误，请检查淘宝/京东登录是否过期！")
      })
    },
    onSort(){
      this.showResultList = this.searchResult.filter(item=>{
        return (this.showTBRes && item.fromwhich==="taobao")||(this.showJDRes && item.fromwhich==="jingdong")
      })
      this.showResultList.sort((a,b)=>{
        return this.price_asc ? a.price - b.price : b.price - a.price
      })
    },
    onFavorKeyword(){
      if(this.searchQuery !== ""){
        axios.post("/api/favorKey",{
          query_name:this.searchQuery,
        },{
          withCredentials: true,
          headers: {
            "content-type": "application/json",
            'X-CSRFTOKEN': this.$cookies.get("csrftoken")
          }
        }).then((res)=>{
          if(res.data==="OK")
            ElMessage.success("成功收藏该商品")
          else if(res.data==="exist")
            ElMessage.error("已收藏过该商品！")
        })
      }
    }
  },

}
</script>

<style scoped>
.logo-search{
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 5vh;
}
.logo-img{
  width: 20vw;

  margin-bottom: 5vh;
}
.front{
  width: 100%;
}
.search-bar{

  display: flex;
  width: 100%;
  justify-content: center;
  flex-direction: row;
}
.control-box{
  margin-top: 20px;
  display: flex;
  width: 100%;
  flex-direction: row;
  justify-content: center;
}
.control-box-1{
  margin-top: 20px;
  display: flex;
  flex-direction: row;
  justify-content: center;
}
.search-bar-cont{
  display: flex;
  align-items: center;
  flex-direction: row;
}
.search-btn{
  margin-left: 10px;
}
.search-bar-bar{

}
.item-list{
  display:flex;
  flex-direction: row;
  width: 100%;
  flex-wrap: wrap;

}
.item-container{
  width:23%;
  margin-left:10px
}
.lists-cont{
  display: flex;
  flex-direction: column;
  align-items: center;

}
.info-cont{
  margin-left: 20px;
  margin-right: 20px;
}
.info-price-text{
  margin-left: 5px;
  font-size: 30px;
  color: #e11414
}
.el-div-d{
  margin-top: 60px
}
.swi-cont{
  display: flex;
  margin-right: 30px;
  margin-left: 30px;
  flex-direction: row;
  align-items: center;
  width: fit-content;
}
.control-btn-box{
  margin-left: 10px;
  margin-right: 10px;
}
.ret-btn-cont{
  margin-left: 20px;
  margin-top: 20px;

}

.ret-btn :hover{
  border-radius: 5px;
  background-color: ghostwhite;
}
.title-text{
  color:#e5633c;
  font-size: 40px;
}

.search-bar-cont > :first-child{
  width: 600px;
}

@media (max-width: 1180px){
  .item-container{
    width:29%;
    margin-left:10px
  }
}

@media (max-width: 960px){
  .item-container{
    width:40%;
    margin-left:10px
  }
}

@media (max-width: 767px) {
  .logo-search{
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 2vh;
  }

  .logo-img{
    width: 20vw;

    margin-bottom: 2vh;
  }


  .search-bar-cont > :first-child{
    width: 200px;
  }
  .search-btn{
    margin-left: 10px;
    width: 100px;
  }
  .logo-img{
    width: 50vw;
  }
  .el-div-d{
    margin-top: 30px
  }
  .title-text{
    padding-left: 20px;
  }





  .item-list{
    display:flex;
    flex-direction: row;
    width: 100%;
    flex-wrap: wrap;

  }
  .item-container{
    width:70%;
    margin-left:10px
  }
  .lists-cont{
    display: flex;
    flex-direction: column;
    align-items: center;

  }
  .info-cont{
    padding-right: 20px;

  }
  .info-price-text{
    margin-left: 5px;
    font-size: 30px;
    color: #e11414
  }
  .swi-cont{
    display: flex;
    margin-right: 30px;
    margin-left: 0px;
    padding-left: 20px;
    flex-direction: row;
    align-items: center;
    width: fit-content;
  }
  .control-box{
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    justify-content: left;
    flex-wrap: wrap;
  }
  .control-box-1{
    margin-top: 20px;
    display: flex;
    flex-direction: row;
    justify-content: center;
    flex-wrap: wrap;
  }

  .control-btn-box{
    margin-right: 10px;
  }
  .control-btn-box > :first-child{
    width: 100px;
    height: 50px;
  }

}

</style>