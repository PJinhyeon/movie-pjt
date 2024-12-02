<template>
  <div class="app-container">
    <header class="app-header">
      <AppNavbar />
    </header>
    <div style="margin-top: 30px;">
      <main class="app-main">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import AppNavbar from '@/components/Common/AppNavbar.vue'
</script>

<style scoped>
/* 전체 페이지 컨테이너 */
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* 전체 화면을 차지 */
  overflow-x: hidden; /* 가로 스크롤 제거 */
  /* background-color: #D19C4A;  */
}

/* 헤더 스타일 */
.app-header {
  position: sticky; /* 스크롤해도 항상 상단에 고정 */
  top: 0;
  z-index: 1000;
  width: 100%;
  /* background-color: #5A3B1F;  */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); /* 약간의 그림자 효과 */
}

/* 메인 컨텐츠 영역 */
.app-main {
  flex: 1; /* 헤더를 제외한 나머지 영역을 차지 */
  /* padding-top: 10px;  */
  padding: 1rem 2rem; /* 콘텐츠 여백 */
  overflow-y: auto; /* 세로 스크롤 가능 */
}
</style>
