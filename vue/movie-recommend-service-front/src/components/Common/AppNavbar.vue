<template>
  <nav>
    <span>홈</span> |
    <span><RouterLink :to="{name: 'MovieListView'}">영화</RouterLink></span> |
    <span>검색</span> |
    <span>추천</span> |
    <span>커뮤니티</span> |
    <span>회원가입</span> |
    <span>로그인</span> |
    <span>마이페이지</span>
  </nav>

</template>

<script setup>
import { RouterLink } from 'vue-router';

RouterLink

</script>

<style scoped>

</style>