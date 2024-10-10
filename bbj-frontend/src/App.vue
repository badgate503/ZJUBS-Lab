<script setup>
import "./assets/App.css";
import LoginPage from "./components/LoginPage.vue";
import axios from "axios";
import { useRouter } from 'vue-router';
const router = useRouter();
axios.get("/api/checkLoginState", {
  withCredentials: true,
  headers: {
    "content-type": "application/json",
    'X-CSRFTOKEN': self.$cookies.get("csrftoken")
  }
}).then(res=>{
  console.log(res)
  if(!res.data["isLogged"]){
    router.push('/login')
  } else {
    router.push('/index')
  }

})



</script>

<template>
  <RouterView />


</template>

<style scoped>
</style>

<script>

</script>