<template>
  <nav>
    <span>홈</span> |
    <span><RouterLink :to="{name: 'MovieListView'}">영화</RouterLink></span> |
    <span>검색</span> |
    <span>추천</span> |
    <span>커뮤니티</span> |
    <RouterLink :to="{ name: 'SignUpView'}">회원가입</RouterLink> |
    <RouterLink v-if="!store.loggedInUser" :to="{ name: 'LoginView' }">로그인</RouterLink> |
    <button v-if="store.isLogin" @click="handleLogout">로그아웃</button> |
    <RouterLink v-if="store.loggedInUser" :to="{ name: 'MyPageView', params: { person_id: store.loggedInUser.pk }}">마이페이지</RouterLink>
  </nav>

</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import { onMounted} from 'vue'

const store = useCounterStore()

const handleLogout = () => {
  store.logOut() // Pinia store의 로그아웃 함수 호출
}

</script>

<style scoped>

</style>