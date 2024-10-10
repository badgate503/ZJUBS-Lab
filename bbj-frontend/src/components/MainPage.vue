

<template>
  <div class="main">
  <el-menu
      default-active="/front"
      class="el-menu-vertical-demo"
      :collapse="isCollapse"
      router :default-active="this.$router.path"
  >
    <el-menu-item index="/front" >
      <el-icon><House /></el-icon>
      <template #title>主页</template>
    </el-menu-item>
    <el-menu-item index="/user">
      <el-icon><User /></el-icon>
      <template #title>我的</template>
    </el-menu-item>
  </el-menu>
    <div class ="content">
      <RouterView/>
    </div>

  </div>
</template>

<style scoped>

</style>

<script>
import axios from "axios";
import "../assets/MainPage.css";
import UserView from "./UserView.vue";
export default {
  components: {UserView},
  data() {
    return {
      username:""
    }
  },
  methods: {
    onlogout() {
      axios.post("/api/logout",{}, {
        withCredentials: true,
        headers: {
          "content-type": "application/json",
          'X-CSRFTOKEN': this.$cookies.get("csrftoken")
        }
      }).then(res=>{
        this.$router.push('/login')
      })
    }
  },
  created() {
    this.$router.push('/front')
    axios.get("/api/checkLoginState", {
      withCredentials: true,
      headers: {
        "content-type": "application/json",
        'X-CSRFTOKEN': this.$cookies.get("csrftoken")
      }
    }).then(res=>{
      console.log(res)
      if(res.data["isLogged"]) {
        this.username = res.data["userName"]
      }

    })
  }

}


</script>