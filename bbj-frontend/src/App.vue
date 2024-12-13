<script setup>
import "./assets/App.css";
import LoginPage from "./components/LoginPage.vue";
import axios from "axios";
import {useRouter} from 'vue-router';
import {onMounted} from 'vue'

const router = useRouter();
axios.get("/api/login").then(res =>{
  console.log(res.data);
  self.$cookies.set("csrftoken", res.data);
});


axios.get("/api/checkLoginState", {
  withCredentials: true,
  headers: {
    "content-type": "application/json",
    'X-CSRFTOKEN': self.$cookies.get("csrftoken")
  }
}).then(res => {
  console.log(res)
  if (!res.data["isLogged"]) {
    router.push('/login')
  } else {
    router.push('/index')
  }
})



onMounted(() => {
  document.body.style.setProperty('--el-color-primary', '#e5633c');
  document.body.style.setProperty('--el-color-primary-light-9', '#fdf5f4');
  document.body.style.setProperty('--el-color-primary-light-3', '#e47b5b');
  document.body.style.setProperty('--el-color-primary-light-5', '#e3957d');
  document.body.style.setProperty('--el-color-primary-dark-2', '#ae5236');
})



</script>

<template>
  <RouterView/>


</template>

<style scoped>
</style>

<script>

</script>