<script setup>

import CollectionPanel from "./CollectionPanel.vue";
</script>

<template>
  <div class="title">我关注的商品</div>
  <el-divider></el-divider>
<CollectionPanel/>
</template>

<style scoped>
.title{
  margin-left: 20px;
  margin-top: 20px;
  font-size: 40px;
}
</style>