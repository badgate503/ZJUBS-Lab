<script setup> </script>

<template>
  <div class="loginPanel">
    <transition name="el-fade-in">
    <div v-show="isLogin" class="loginContent">
      <div class="textWarp">
        <div class="loginText">
          Sign in
        </div>
      </div>
      <el-divider><el-icon><user /></el-icon></el-divider>
      <div class="fieldWarp">
        <el-row :gutter="30">
          <el-col :span="24">
            <el-input
                v-model="logInfo.email"
                size="large"
                clearable
                @focusout="validateEmail"
                @click="onEmailChange"
                @change="onEmailChange"
                placeholder="邮箱"
            ></el-input>
          </el-col>
          <el-collapse-transition>
          <el-col v-show="isMailInvalid" :span="7">
            <el-text type="danger" size="small">邮箱格式有误</el-text>
          </el-col>
          </el-collapse-transition>
          <el-col :span="24">
            <el-input
                v-model="logInfo.password"
                size="large"
                clearable
                show-password
                placeholder="密码"
            />
          </el-col>
          <el-col :span="24">
            <ElButton class="loginBtn" size="large" @click="OnLogin">登录</ElButton>
          </el-col>
        </el-row>
      </div>
      <el-divider style="margin-top: 50px">or</el-divider>
      <el-col :span="24">
        <ElButton class="loginBtn" size="large" @click="gotoRegister">还没账号，立即注册</ElButton>
      </el-col>
    </div>
    </transition>


    <transition name="el-fade-in">
    <div v-show="isRegister" class="loginContent">
      <div class="textWarp">
        <div class="loginText">
          Sign up
        </div>
      </div>
      <el-divider><el-icon><user /></el-icon></el-divider>
      <div class="fieldWarp">
        <el-row :gutter="30">
          <el-col :span="24">
            <el-input
                v-model="logInfo.nickname"
                size="large"
                clearable

                placeholder="昵称"
            ></el-input>
          </el-col>
          <el-col :span="24">
            <el-input
                v-model="logInfo.email"
                size="large"
                clearable
                @focusout="validateEmail"
                @click="onEmailChange"
                @change="onEmailChange"
                placeholder="邮箱"
            ></el-input>
          </el-col>
          <el-collapse-transition>
            <el-col v-show="isMailInvalid" :span="7">
              <el-text type="danger" size="small">邮箱格式有误</el-text>
            </el-col>
          </el-collapse-transition>
          <el-col :span="24">
            <el-input
                v-model="logInfo.password"
                size="large"
                clearable
                show-password
                placeholder="密码"
                @focusout="validatePwd"
                @click="onPwdChange"
                @change="onPwdChange"
            />
          </el-col>
          <el-collapse-transition>
            <el-col v-show="isPwdInvalid" :span="16">
              <el-text type="danger" size="small">八个字符以上，且至少有一个字母和一个数字</el-text>
            </el-col>
          </el-collapse-transition>
            <el-col :span="24">
              <el-input
                  v-model="logInfo.passwordagain"
                  size="large"
                  clearable
                  show-password
                  placeholder="再次输入密码"
                  @focusout="validatePwdAgain"
                  @click="onPwdAgainChange"
                  @change="onPwdAgainChange"
              />
            </el-col>
          <el-collapse-transition>
            <el-col v-show="isPwdAgainInvalid" :span="8">
              <el-text type="danger" size="small">两次输入密码不同</el-text>
            </el-col>
          </el-collapse-transition>
            <el-col :span="24">
              <ElButton class="loginBtn" size="large" @click="OnRegister">注册</ElButton>
            </el-col>
        </el-row>
      </div>
      <el-divider style="margin-top: 50px">or</el-divider>
      <el-col :span="24">
        <ElButton class="loginBtn" size="large" @click="gotoLogin">已有账号，立即登录</ElButton>
      </el-col>
    </div>
    </transition>
  </div>

</template>

<style scoped>

</style>



<script lang="jsx">
import axios from "axios";
import "../assets/LoginPage.css";

import Qs from 'qs';


export default {
  data() {
    return {
      text:"hi",
      logInfo: {
        email: null,
        password: null,
        nickname: null,
        passwordagain: null
      },
      isMailInvalid: false,
      isPwdInvalid: false,
      isPwdAgainInvalid: false,
      isRegister: false,
      isLogin: true
    }
  },
  methods: {



    isEmail(str){
      var reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/;
      return reg.test(str);
    },
    isValidPwd(str){
      var reg = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/
      return reg.test(str);
    },

    OnLogin() {
      var that = this;
      if(this.isMailInvalid) {
        ElMessage.error('邮箱格式错误')
        return
      }
      if(this.logInfo.email === null || this.logInfo.email === '') {
        ElMessage.error('请输入注册时使用的邮箱')
        return
      }
      else if(this.logInfo.password === null || this.logInfo.password === '') {
        ElMessage.error('请输入密码')
        return
      }
      let data = new FormData()
      data.append('username',this.logInfo.email)
      data.append('password',this.logInfo.password)
      axios.post("/api/login",data,{
        withCredentials: true,
        headers: {
          "content-type": "application/json",
          'X-CSRFTOKEN': this.$cookies.get("csrftoken")
        }
      }).then(response => {
        console.log(response.data['isLoginOK'])
        if(response.data['isLoginOK']) {
          ElMessage.success(response.data['userName']+'，欢迎回来！')
          this.$router.push('/index')
        } else {
          ElMessage.error('用户不存在或密码错误')
        }
      })
    },

    OnRegister() {
      if(this.logInfo.nickname===null || this.logInfo.nickname==='') {
        ElMessage.error('请输入昵称')
        return
      }
      if(this.isMailInvalid) {
        ElMessage.error('邮箱格式错误')
        return
      }
      if(this.logInfo.email === null || this.logInfo.email === '') {
        ElMessage.error('请输入邮箱')
        return
      }
      if(this.logInfo.password === null || this.logInfo.password === '') {
        ElMessage.error('请输入密码')
        return
      }
      if(this.isPwdInvalid) {
        ElMessage.error('密码安全性较低')
        return
      }
      if(this.logInfo.passwordagain === null || this.logInfo.passwordagain === '') {
        ElMessage.error('请再次输入密码')
        return
      }
      if(this.logInfo.passwordagain !== this.logInfo.password) {
        ElMessage.error('两次输入的密码不同')
        return
      }
      axios.post("/api/register",{
        "username":this.logInfo.email,
        "pwd":this.logInfo.password,
        "nickname":this.logInfo.nickname
      },{
        withCredentials: true,
        headers: {
          "content-type": "application/json",
          'X-CSRFTOKEN': this.$cookies.get("csrftoken")
        }
      }).then(response => {
        if(response.data['isRegisterOK']) {
          ElMessage.success('成功注册')
          this.$router.push('/index')
        } else {
          ElMessage.error('该邮箱已注册')
        }
      })
    },

    validateEmail(){
      this.isMailInvalid = false;
      if(this.logInfo.email === null || this.logInfo.email === '') return;
      if(!this.isEmail(this.logInfo.email)) {
        this.isMailInvalid = true
      }
    },
    validatePwd(){
      this.isPwdInvalid = false;
      if(this.isLogin) return;  // Don't do password verification.
      if(this.logInfo.password === null || this.logInfo.password === '') return;
      console.log("jj")
      if(!this.isValidPwd(this.logInfo.password)) {
        this.isPwdInvalid = true
      }
      this.validatePwdAgain()
    },
    validatePwdAgain(){
      this.isPwdAgainInvalid = false;
      if(this.isLogin) return;
      if(this.logInfo.password === null || this.logInfo.password === '') return;
      if(this.logInfo.passwordagain === null || this.logInfo.passwordagain === '') return;
      if(this.isPwdInvalid) return;
      if(this.logInfo.passwordagain !== this.logInfo.password) {
        this.isPwdAgainInvalid = true;
      }
    },
    onPwdChange(){
      this.isPwdAgainInvalid = false;
      this.isPwdInvalid = false;
    },
    onPwdAgainChange(){
      this.isPwdAgainInvalid = false;
    },
    onEmailChange(){
      this.isMailInvalid = false;
    },
    sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    },
    async gotoRegister(){
      this.isLogin = false;
      await this.sleep(200)
      this.isRegister = true;
    },
    async gotoLogin(){
      this.isRegister = false;
      await this.sleep(200)
      this.isLogin = true;
    }
  },
}
</script>