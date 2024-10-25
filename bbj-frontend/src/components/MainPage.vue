

<template>
  <div class="main">
  <el-menu
      default-active="/front"
      class="el-menu-vertical-demo"
      :collapse="isCollapse"
      router :default-active="this.$router.path"

  >
    <el-menu-item index="/front" >
      <el-icon><img alt="logo" src="../assets/logo.svg"></el-icon>
      <template #title>比比价主页</template>
    </el-menu-item>
    <el-menu-item index="/collect" >
      <el-icon><Star /></el-icon>
      <template #title>我关注的</template>
    </el-menu-item>
    <el-popover placement="right-end" :width="400" trigger="click">
      <template #reference>
    <el-menu-item class="user">
      <el-icon><User /></el-icon>
    </el-menu-item>
      </template>
      <div class="pop">
      <div class="userInfoHolder">

        <el-avatar :size="70" :src="circleUrl" />

        <div class="infoHolder">
          <div class="userName">
            {{ curUser.userName }}
          </div>

          <div class="userEmail">
            <el-icon><Message /></el-icon>
            <div class="textEmail">
              {{ curUser.userEmail }}
            </div>

          </div>
        </div>


      </div>
      <div class="logoutBtn">
        <ElButton type="danger" @click="onlogout">Log out</ElButton>
      </div>
      </div>
    </el-popover>

  </el-menu>
    <div class ="content" >
      <RouterView/>
    </div>

  </div>
</template>

<style scoped>
.content{
  flex-grow: 1;
}
.user{
  margin-top: calc(100vh - 200px);
}
.userInfoHolder{
  display: flex;
  flex-direction: row;
  align-items: center;
}
.userName{
  font-size: 30px;
  font-weight: bold;
}
.userEmail{
  margin-left: 2px;
  font-size: 15px;
  display: flex;
  flex-direction: row;
  align-items: center;
}
.textEmail{
  margin-left: 5px;
}
.infoHolder{
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-left: 10px;
}
.pop{
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.logoutBtn{
  margin-top: 15px;
  width: 100vw;
  margin-left: 5px;
}
.logoutBtn ElButton {
  width: 100vw;
}
</style>

<script>
import axios from "axios";
import "../assets/MainPage.css";
import UserView from "./UserView.vue";
import {getCurrentUser} from "../utils.js";

export default {
  components: {UserView},
  data() {
    return {
      curUser:{
        userName:"",
        userEmail:"",
      },
      isCollapse:true
    }
  },
  methods: {
    onlogout() {
      axios.post("/api/logout", {}, {
        withCredentials: true,
        headers: {
          "content-type": "application/json",
          'X-CSRFTOKEN': this.$cookies.get("csrftoken")
        }
      }).then(res => {
        this.$router.push('/login')
      })
    }

  },
  async created() {
    this.$router.push('/front')
    var res = await getCurrentUser(this)
    this.curUser.userName = res["userName"]
    this.curUser.userEmail = res["userEmail"]
  },


}


</script>