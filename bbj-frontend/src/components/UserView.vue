<script setup>

</script>

<template>
  Hello, {{ username }}
  <ElButton @click="onlogout">Log out</ElButton>
</template>

<style scoped>

</style>

<script>
import axios from "axios";
import MainPage from "./MainPage.vue";
import {getCurrentUser} from "../utils.js";

export default {
  data() {
    return {
      username: ""
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
    this.username = await getCurrentUser(this)
  }

}
</script>