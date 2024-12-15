

<template>
  <div v-show="!deleted" class="collection-main">

    <el-card shadow="always"class="coll-container">
      <div class="name-price">
        <div class="name-icon">
          <el-icon size="large"><Discount /></el-icon><div class="item-name">{{ info.keyInfo.keyword_name }}</div>
        </div>
        <div class="price">¥{{ (parseFloat(info.keyInfo.minPrice)/100).toFixed(2) }} ~ ¥{{(parseFloat(info.keyInfo.maxPrice)/100).toFixed(2)}}</div>
      </div>
      <div class="item-info">
        <div class="item-num">共找到商品 {{info.keyInfo.JDcount+info.keyInfo.TBcount}} 件</div>
      </div>
      <div class="operations">
        <el-button-group>
          <el-button type="warning" @click="handleDetail">查看详情</el-button>
          <el-button type="primary" @click="removeFavor">
            取消收藏
          </el-button>
        </el-button-group>
      </div>



    </el-card>




  </div>
  <el-dialog
      v-model="showDetail"
      :title="'“'+info.keyInfo.keyword_name+'“的商品信息'"
      width="95%"
      :before-close="handleCancelLoginTaobao"
      style="display: flex; flex-direction: column"
  >
    <div class="top-cont">
      
    
    <div class="detail-price-cont">
      
      <div class="info-cont">
        <el-text size="large">当前淘宝平均价格</el-text>
        <a class="info-price-text">¥{{parseFloat(info.keyInfo.TBavgPrice/100).toFixed(2)}}</a>
      </div>
      <div class="info-cont">
        <el-text size="large">当前京东平均价格</el-text>
        <a class="info-price-text">¥{{parseFloat(info.keyInfo.JDavgPrice/100).toFixed(2)}}</a>
      </div>
      <div class="info-cont">
        <el-text size="default">更新时间：{{info.keyInfo.update_time}}</el-text>
      </div>
    </div>
    <div class="price-detail">¥{{ (parseFloat(info.keyInfo.minPrice)/100).toFixed(2) }} ~ ¥{{(parseFloat(info.keyInfo.maxPrice)/100).toFixed(2)}}</div>
    </div>

    <div class="chart-cont">
      <v-chart autoresize :option="chartOption" style="height: 400px"></v-chart>
    </div>


    <template #footer>
      <div class="dialog-footer">
        <div class="switch-cont">
          <el-text style="margin-right:10px;">邮件通知价格更新</el-text>
          <el-switch  size="large" v-model="info.need_notify" @change="onEditNeedNotify"></el-switch>
        </div>
        <div>
          <el-button  type="primary" @click="gotoLink">去往最低价商品购买页</el-button>
          <el-button @click="showDetail=false">关闭</el-button>
        </div>

      </div>
    </template>
  </el-dialog>
</template>
<script>

import axios from "axios";
import ECharts from "vue-echarts";
import {ElMessage} from "element-plus";
import * as Echarts from "echarts";
export default {
  data() {
    return {
      deleted:false,
      showDetail:false,
      chartOption:{
        title:{
          text:"价格走势图"
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          }
        },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: [],
            axisLabel:{
              formatter: function (params) {
                var val = "";
                //判断长度
                if (params.length > 4) {
                  //替换原字符
                  val = params.substr(0, 4) + '...';
                  //返回
                  return val;
                } else {
                  //否则返回原string
                  return params;
                }
              }
            }
          },
          yAxis: {
            type: 'value'
          },
        legend: {
          data: ['淘宝均价变化','京东均价变化','最低价格变化'],
          right: '10',
          top: '20'
        },
          series: [
            {
              name:"淘宝均价变化",
              label: {
                show: true,
                position: 'top'
              },
              data: [],
              type: 'line',
              smooth: true
            },
            {
              name:"京东均价变化",
              label: {
                show: true,
                position: 'top'
              },
              data: [],
              type: 'line',
              smooth: true
            },
            {
              name:"最低价格变化",
              label: {
                show: true,
                position: 'top'
              },
              data: [],
              type: 'line',
              smooth: true
            }
          ],
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
      }
    }
  },
  props: {
    info:Object,
    removePanel:Function,
  },
  mounted() {
    console.log(this.info)
  },
  methods: {


    removeFavor(){
      axios.post('/api/remove_favor', {
        query_name:this.info.keyInfo.keyword_name
      },{
        withCredentials: true,
        headers: {
          "content-type": "application/json",
          'X-CSRFTOKEN': this.$cookies.get("csrftoken")
        }
      }).then(res=>{
        if(res.data==="OK"){
          ElMessage.success("取消收藏成功！")
        }else{
          ElMessage.error("取消收藏失败!")
        }
        this.deleted=true
      })
    },
    handleDetail(){
      axios.post('/api/get_price_change',{
        query_name: this.info.keyInfo.keyword_name,
      },{
        withCredentials: true,
        headers: {
          "content-type": "application/json",
          'X-CSRFTOKEN': this.$cookies.get("csrftoken")
        }
      }).then(res=>{
        let priceChange = res.data
        this.chartOption.xAxis.data = priceChange.map(iter=>iter.update_time)
        this.chartOption.series[0].data = priceChange.map(iter=>parseFloat(iter.TBavgPrice/100).toFixed(2))
        this.chartOption.series[1].data = priceChange.map(iter=>parseFloat(iter.JDavgPrice/100).toFixed(2))
        this.chartOption.series[2].data = priceChange.map(iter=>parseFloat(iter.minPrice/100).toFixed(2))
        console.log(this.chartOption)
      })
      this.showDetail = true
    },
    onEditNeedNotify(){
      axios.post('/api/favor_notify', {
        query_name: this.info.keyInfo.keyword_name,
        new_need: this.info.need_notify
      },{
        withCredentials: true,
        headers: {
          "content-type": "application/json",
          'X-CSRFTOKEN': this.$cookies.get("csrftoken")
        }
      }).then(res=>{
        if(res.data==="OK")
          ElMessage.success("成功修改")
      })
    },
    gotoLink(){
      window.location.href= this.info.lowest_link
    }
  },



}

</script>
<style scoped>

.coll-container{
  margin-left: 20px;
  margin-top: 20px;

}
.switch-tab{
  margin-top: 10px;
}
.item-name{
  font-size: large;
  margin-left: 5px;
}
.name-price{
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
  font-size: x-large;
  color: #cf2020;
}
.price-detail{
  font-size: xx-large;
  color: #cf2020;
  margin-top: 10px;
  margin-right: 10px;
}
.item-num{
  font-size: small;
  color: #9a9a9a;
}
.operations{
  margin-top:10px;
}
.chart-cont{
  margin-top:20px;
  width:100%;
}
.info-price-text{
  margin-left: 5px;
  color: #e11414
}
.info-cont{
  margin-top: 10px;
}
.top-cont{
  display: flex;
  flex-direction: row;

  justify-content: space-between;
}
.dialog-footer{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
}

.switch-cont > :last-child{
  margin-right: 20px;
}

@media (max-width: 860px){

}

@media (max-width: 808px){
  .operations{
    display: flex;
    flex-direction: column;
    align-items: flex-end;
  }
  .price-detail{
    font-size: large;
    color: #cf2020;
    margin-top: 10px;
    margin-right: 10px;
  }
  .dialog-footer{
    display: flex;
    flex-direction: column;
    align-items: flex-end;
  }
  .switch-cont > :last-child{
    margin-right: 0px;
  }
}
</style>