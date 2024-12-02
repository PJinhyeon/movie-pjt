<template>
  <nav :class="['navbar', { 'navbar-scrolled': isScrolled }]">
    <div class="navbar-logo">
      <RouterLink :to="{ name: 'HomeView' }" style="font-weight: 5000; font-size: xx-large;">CHU:P</RouterLink>
    </div>
    <div class="navbar-menu">
      <RouterLink
        class="navbar-link"
        :class="{ active: isActive('HomeView'), 'scrolled-link': isScrolled }"
        :to="{ name: 'HomeView' }"
      >
        HOME
      </RouterLink>
      <RouterLink
        class="navbar-link"
        :class="{ active: isActive('MovieListView'), 'scrolled-link': isScrolled }"
        :to="{ name: 'MovieListView' }"
      >
        MOVIES
      </RouterLink>
      <RouterLink
        class="navbar-link"
        :class="{ active: isActive('SearchView'), 'scrolled-link': isScrolled }"
        :to="{ name: 'SearchView' }"
      >
        SEARCH
      </RouterLink>
      <RouterLink
        class="navbar-link"
        :class="{ active: isActive('CommunityView'), 'scrolled-link': isScrolled }"
        :to="{ name: 'CommunityView' }"
      >
        COMMUNITY
      </RouterLink>
      <RouterLink
        class="navbar-link"
        :class="{ active: isActive('RecommendationView'), 'scrolled-link': isScrolled }"
        :to="{ name: 'RecommendationView' }"
      >
        RECOMMENDATIONS
      </RouterLink>
      <RouterLink
        v-if="!store.loggedInUser"
        class="navbar-link"
        :class="{ active: isActive('SignUpView'), 'scrolled-link': isScrolled }"
        :to="{ name: 'SignUpView' }"
      >
        SIGNUP
      </RouterLink>
      <RouterLink
        v-if="!store.loggedInUser"
        class="navbar-link"
        :class="{ active: isActive('LoginView'), 'scrolled-link': isScrolled }"
        :to="{ name: 'LoginView' }"
      >
        LOGIN
      </RouterLink>
      <a
        v-if="store.isLogin"
        class="navbar-link logout-link"
        :class="{ 'scrolled-link': isScrolled }"
        @click.prevent="handleLogout"
      >
        LOGOUT
      </a>
      <RouterLink
        v-if="store.loggedInUser"
        class="navbar-link"
        :class="{ active: isActive('MyPageView'), 'scrolled-link': isScrolled }"
        :to="{ name: 'MyPageView', params: { person_id: store.loggedInUser.pk } }"
      >
        MYPAGE
      </RouterLink>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink, useRoute } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import { ref, onMounted, onUnmounted } from 'vue'

const store = useCounterStore()
const route = useRoute()

const isScrolled = ref(false)

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
}

const isActive = (routeName) => {
  return route.name === routeName
}

const handleLogout = () => {
  store.logOut() // Pinia store의 로그아웃 함수 호출
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
/* 네비게이션 스타일 */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  padding: 1rem 2rem;
  z-index: 1000;
}

/* 로고 스타일 */
.navbar-logo {
  margin-right: 2rem;
}

.navbar-logo a {
  font-family: 'Noto Sans KR', sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: #FFE474;
  text-decoration: none;
}

/* 메뉴 스타일 */
.navbar-menu {
  display: flex;
  gap: 1.5rem;
}

/* 메뉴 링크 */
.navbar-link {
  font-family: 'Noto Sans KR', sans-serif;
  font-size: 1rem;
  font-weight: 400;
  text-decoration: none;
  color: #FFFFFF;
  padding: 0.5rem 1rem;
  border-radius: 30px;
  transition: background-color 0.2s ease;
}

/* 호버 효과 */
.navbar-link:hover {
  color: #FFE474;
}

/* 활성화된 메뉴 스타일 */
.navbar-link.active {
  background-color: #FFE474;
  color: #572200;
  font-weight: 700;
}

/* 스크롤된 상태에서 외곽선 추가 */
.scrolled-link {
  -webkit-text-stroke: 0.5px #572200;
}
</style>
