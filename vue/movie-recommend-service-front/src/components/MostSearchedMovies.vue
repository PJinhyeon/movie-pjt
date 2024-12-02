<template>
  <div class="most-searched-movies">
    <div v-if="loading" class="loading-indicator">Loading...</div>
    <div v-else class="movie-list">
      <MovieCard
        v-for="movie in movies"
        :key="movie.id"
        :movie="movie"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import MovieCard from '@/components/MovieCard.vue';

const movies = ref([]);
const loading = ref(true);

// 많이 검색된 영화 데이터 가져오기
const fetchMostSearchedMovies = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/search-history/topsearch/');
    movies.value = response.data; // 데이터를 Vue 상태로 저장
  } catch (error) {
    console.error('Error fetching most searched movies:', error);
  } finally {
    loading.value = false; // 로딩 상태 종료
  }
};

// 컴포넌트 로드 시 데이터 가져오기
onMounted(fetchMostSearchedMovies);
</script>

<style scoped>
.most-searched-movies {
  margin: 20px 0;
  text-align: center;
}

.loading-indicator {
  font-size: 1.5rem;
  color: gray;
}

.movie-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: center;
}
</style>
