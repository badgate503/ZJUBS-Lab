<script setup>

</script>

<template>
  <div class="front">
    <div class="logo-search">
      <img class="logo-img"alt="logo" src="../assets/logo_txt.svg"></img>
      <div class="search-bar">

        <div class="search-bar-cont">

          <el-input
              class="search-bar-bar"
              v-model="input1"
              style="width: 600px"
              size="large"
              clearable
              placeholder="Please Input"
          />
          <el-button  class="search-btn" size="large" type="primary"><el-icon size="large"><Search/></el-icon></el-button>

        </div>

      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios";
import {getCurrentUser} from "../utils.js";
import { Search } from '@element-plus/icons-vue'

export default {
  data() {

  },
  methods: {
    onClick() {
      axios.get('/api/send_email')
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
}
.front{
  width: 100%;
}
.search-bar{
  display: flex;
  width: 100%;
  justify-content: center;
  flex-direction: row;
  margin-top: 5vh;
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
</style>