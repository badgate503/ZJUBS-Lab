

<template>
  Hello, {{ username }}
</template>

<style scoped>

</style>

<script>
import axios from "axios";
export default {
  data() {
    return {
      username:""
    }
  },
  methods: {

  },
  created() {
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