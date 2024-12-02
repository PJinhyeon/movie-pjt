<template>
  <div class="page-container">
    <!-- 추천 영화 캐러셀 추가 -->
    <MainPageCarousel @click="goToRecommendation" />
    <div>
      <h2>인기 영화 TOP10</h2>
      <PopularMovieList />
      <h2>게시글이 많이 쓰여진 영화 TOP6</h2>
      <ManyAriticlesList />
      <h2>많이 검색한 영화</h2>
      <MostSearchedMovies/>
      <!-- 많이 검색한 영화 보여주기 -->
      <h2>나의 찜 목록</h2>
      <CartView />
    </div>
  </div>
</template>

<script setup>
import CartView from '@/views/CartView.vue';
import MainPageCarousel from '@/components/MainPageCarousel.vue';
import ManyAriticlesList from '@/components/ManyAriticlesList.vue';
import PopularMovieList from '@/components/PopularMovieList.vue';
import { useRouter } from 'vue-router';
import MostSearchedMovies from '@/components/MostSearchedMovies.vue';

// Vue Router 설정
const router = useRouter();

const goToRecommendation = () => {
  router.push({ name: 'RecommendationView' }); // 'RecommendationView'로 이동
};
</script>

<style scoped>
/* HomeView.vue는 페이지 특화 스타일만 포함 */
</style>
