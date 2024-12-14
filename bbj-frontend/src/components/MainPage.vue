

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

          <div class="login-state">
            <el-tag type="primary" v-show="isTBLogin">已登录淘宝</el-tag>
            <el-tag type="primary" style="margin-left: 10px;" v-show="isJDLogin">已登录京东</el-tag>
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
        <el-button-group>
          <ElButton type="warning" @click="onlogTaobao">登录淘宝</ElButton>
          <ElButton type="warning" @click="onlogJindong">登录京东</ElButton>
        </el-button-group>

        <ElButton style="margin-left:10px" type="danger" @click="onlogout">退出登录</ElButton>
      </div>
      </div>
    </el-popover>

  </el-menu>
    <div class ="content" >
      <ElScrollbar>
        <RouterView/>
      </ElScrollbar>

    </div>

  </div>
  <el-dialog
      v-model="dialogVisible"
      :title="'登录'+name"
      width="500"
      :before-close="handleCancelLoginTaobao"
  >

    <div class="qr-cont">
      <el-text size="large">请使用手机{{name}}扫码登录</el-text>
      <div  class ="qrcode">
        <el-image v-loading="QRLoading" :src="QRSrc" alt="QRcode" ></el-image>
      </div>
    </div>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleCancelLoginTaobao">Cancel</el-button>
      </div>
    </template>
  </el-dialog>
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
.qr-cont{
  width:100%;
  display:flex;
  flex-direction: column;
  align-items: center;
}
.qrcode{
  width: fit-content;
  margin-top:20px;
}
</style>

<script>
import axios from "axios";
import "../assets/MainPage.css";
import UserView from "./UserView.vue";
import {getCurrentUser} from "../utils.js";
import {ElMessage} from "element-plus";

export default {
  components: {UserView},
  data() {
    return {
      curUser:{
        userName:"",
        userEmail:"",
      },
      isTBLogin:false,
      isJDLogin:false,
      name:"淘宝",
      isCollapse:true,
      dialogVisible:false,
      QRLoading:true,
      QRSrc:"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMMAAADDCAYAAAA/f6WqAAAACXBIWXMAABYlAAAWJQFJUiTwAAAE9GlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgOS4xLWMwMDIgNzkuYjdjNjRjY2Y5LCAyMDI0LzA3LzE2LTEyOjM5OjA0ICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1sbnM6cGhvdG9zaG9wPSJodHRwOi8vbnMuYWRvYmUuY29tL3Bob3Rvc2hvcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjYuMSAoTWFjaW50b3NoKSIgeG1wOkNyZWF0ZURhdGU9IjIwMjQtMTItMDhUMTM6NTM6MDkrMDg6MDAiIHhtcDpNb2RpZnlEYXRlPSIyMDI0LTEyLTA4VDEzOjU2OjAyKzA4OjAwIiB4bXA6TWV0YWRhdGFEYXRlPSIyMDI0LTEyLTA4VDEzOjU2OjAyKzA4OjAwIiBkYzpmb3JtYXQ9ImltYWdlL3BuZyIgcGhvdG9zaG9wOkNvbG9yTW9kZT0iMyIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDowOGZlZjk4MC1kOWYyLTQyOTItOTNmNy02MzlmNzRiZDk5ZTUiIHhtcE1NOkRvY3VtZW50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"
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
    },

    async onlogTaobao() {
      this.name = "淘宝"
      this.QRLoading = true;
      this.dialogVisible = true;
      await axios.post("/api/tb_get_qrcode", {}, {
        withCredentials: true,
        headers: {
          "content-type": "application/json",
          'X-CSRFTOKEN': this.$cookies.get("csrftoken")
        }
      }).then(res => {
        console.log(res)
        if (res.data.status === "success") {
          this.QRSrc = `data:image/png;base64,${res.data.img}`;
          this.QRLoading = false;

        } else {
          axios.post("/api/close_driver", {}, {
            withCredentials: true,
            headers: {
              "content-type": "application/json",
              'X-CSRFTOKEN': this.$cookies.get("csrftoken")
            }
          })
        }
      })
      await axios.post("/api/tb_get_cookie", {}, {
        withCredentials: true,
        headers: {
          "content-type": "application/json",
          'X-CSRFTOKEN': this.$cookies.get("csrftoken")
        }
      }).then(res => {
        console.log(res)
        if (res.data.status === "success") {
          console.log("OK")
          this.QRLoading = true;
          this.dialogVisible = false;
          ElMessage({
            message: '淘宝登录成功！',
            type: 'success',
          })
        } else {
          ElMessage({
            message: '登录失败',
            type: 'warning',
          })
        }
      })
    },


    handleCancelLoginTaobao() {
      this.QRLoading = true;
      this.dialogVisible = false;
      axios.post("/api/close_driver", {}, {
        withCredentials: true,
        headers: {
          "content-type": "application/json",
          'X-CSRFTOKEN': this.$cookies.get("csrftoken")
        }
      })
    },

    async onlogJindong() {
      this.name = "京东"
      this.QRLoading = true;
      this.dialogVisible = true;
      await axios.post("/api/jd_get_qrcode", {}, {
        withCredentials: true,
        headers: {
          "content-type": "application/json",
          'X-CSRFTOKEN': this.$cookies.get("csrftoken")
        }
      }).then(res => {
        console.log(res)
        if (res.data.status === "success") {
          this.QRSrc = `data:image/png;base64,${res.data.img}`;
          this.QRLoading = false;

        } else {
          axios.post("/api/close_driver", {}, {
            withCredentials: true,
            headers: {
              "content-type": "application/json",
              'X-CSRFTOKEN': this.$cookies.get("csrftoken")
            }
          })
        }
      })
      await axios.post("/api/jd_get_cookie", {}, {
        withCredentials: true,
        headers: {
          "content-type": "application/json",
          'X-CSRFTOKEN': this.$cookies.get("csrftoken")
        }
      }).then(res => {
        console.log(res)
        if (res.data.status === "success") {
          console.log("OK")
          this.QRLoading = true;
          this.dialogVisible = false;
          ElMessage({
            message: '京东登录成功！',
            type: 'success',
          })
        } else {
          ElMessage({
            message: '登录失败',
            type: 'warning',
          })
        }
      })
    },
  },
  async created() {
    this.$router.push('/front')
    var res = await getCurrentUser(this)
    this.curUser.userName = res["userName"]
    this.curUser.userEmail = res["userEmail"]
    this.isTBLogin = res["userTBLogged"]
    this.isJDLogin = res["userJDLogged"]
  },


}


</script>