<template>
  <div class="recommended-grid">
    <!-- 로딩 상태 -->
    <div v-if="isLoading" class="loading">
      <p>추천받은 영화를 불러오는 중입니다...</p>
    </div>
    <!-- 추천받은 영화 목록 -->
    <div v-else-if="recommendedMovies.length" class="grid">
      <MovieCard
        v-for="movie in recommendedMovies"
        :key="movie.id"
        :movie="movie"
      />
    </div>
    <!-- 추천 영화 없음 -->
    <div v-else>
      <p>추천받은 영화가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import MovieCard from '@/components/MovieCard.vue';

const recommendedMovies = ref([]); // 최종 영화 데이터를 저장
const isLoading = ref(true); // 로딩 상태 관리
const error = ref(null); // 에러 상태 관리

const fetchMovieDetails = async (movieId) => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/movies/${movieId}/`);
    return response.data; // 영화 데이터 반환
  } catch (err) {
    console.error(`영화 ID ${movieId}의 데이터를 불러오는 중 오류 발생:`, err);
    return null; // 실패 시 null 반환
  }
};

onMounted(async () => {
  try {
    // 추천받은 영화 ID 목록 가져오기
    const response = await axios.get('http://127.0.0.1:8000/recommendations/recommendations/user/', {
      headers: {
        Authorization: `Token ${localStorage.getItem('authToken')}`,
      },
    });

    const movieIds = response.data.map((item) => item.movie); // 영화 ID 추출

    // 영화 ID를 기반으로 상세 데이터 가져오기
    const movieRequests = movieIds.map((movieId) => fetchMovieDetails(movieId));
    const movies = await Promise.all(movieRequests); // 병렬 요청 처리

    // null이 아닌 데이터만 저장
    recommendedMovies.value = movies.filter((movie) => movie !== null);
  } catch (err) {
    console.error('추천받은 영화 로드 실패:', err);
    error.value = '추천받은 영화를 불러오는 중 문제가 발생했습니다.';
  } finally {
    isLoading.value = false; // 로딩 완료
  }
});
</script>

<style scoped>
.recommended-grid {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
  width: 100%;
  max-width: 1200px;
  display: flex;
  flex-wrap: wrap;
}

.loading,
p {
  color: #fff;
  text-align: center;
  margin-top: 20px;
}
</style>
