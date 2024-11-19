<template>
  <nav>
    <span>홈</span> |
    <span>영화</span> |
    <span>검색</span> |
    <span>추천</span> |
    <span>커뮤니티</span> |
    <RouterLink :to="{ name: 'SignUpView'}">회원가입</RouterLink> |
    <RouterLink :to="{ name: 'LoginView' }">로그인</RouterLink> |
    <span>마이페이지</span>
  </nav>

</template>

<script setup>
import { RouterLink } from 'vue-router'

</script>

<style scoped>

</style>