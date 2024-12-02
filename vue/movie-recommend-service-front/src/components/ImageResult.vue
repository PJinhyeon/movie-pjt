<template>
  <div class="movie-list">
    <MovieCard 
      v-for="movie in props.movies" 
      :key="movie.id" 
      :movie="movie" 
    />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import axios from 'axios';
import MovieCard from '@/components/MovieCard.vue';

// 부모로부터 추천 영화 데이터를 props로 받음
const props = defineProps({
  movies: {
    type: Array,
    default: () => []
  }
});

// 부모에게 이벤트 전달
const emit = defineEmits(['updateMovies']);

// 상태 관리
const savingRecommendation = ref(false);
const savedMovies = ref([]); // 이미 저장된 영화 목록을 관리

// 로컬 스토리지에서 토큰 가져오기
const token = localStorage.getItem('authToken'); // 'authToken'은 토큰 저장 키 이름

// 추천 결과를 모두 저장하는 함수
const saveAllRecommendations = (newMovies) => {
  // 새롭게 추가된 영화만 저장
  const moviesToSave = newMovies.filter((movie) => !savedMovies.value.includes(movie.id));

  if (savingRecommendation.value || !moviesToSave.length) return; // 중복 요청 방지 및 저장할 영화 없음

  savingRecommendation.value = true;

  // 추천 영화 리스트 저장 요청
  const requests = moviesToSave.map((movie) =>
    axios.post(
      'http://127.0.0.1:8000/recommendations/recommendations/',
      { movie: movie.id },
      {
        headers: {
          Authorization: `Token ${token}`, // 헤더에 토큰 추가
        },
      }
    )
  );

  Promise.all(requests)
    .then((responses) => {
      // 저장된 영화들을 부모로 전달하고 목록 업데이트
      responses.forEach((response) => {
        savedMovies.value.push(response.data.id);
        emit('updateMovies', response.data);
      });
      alert('모든 추천 영화가 저장되었습니다!');
    })
    .catch((error) => {
      console.error('저장 실패:', error);
    })
    .finally(() => {
      savingRecommendation.value = false;
    });
};

// 추천 영화가 변경되면 새로 추가된 영화만 저장
watch(
  () => props.movies,
  (newMovies) => {
    saveAllRecommendations(newMovies);
  },
  { immediate: true } // 컴포넌트가 렌더링될 때도 실행
);
</script>

<style scoped>
.movie-list {
  display: flex;
  flex-wrap: wrap; /* 여러 줄로 카드 배치 */
  gap: 20px; /* 카드 간 간격 */
  justify-content: center; /* 가로 중앙 정렬 */
  padding: 20px;
}

.movie-card {
  opacity: 0;
  transform: translateY(-20px); /* 위에서 아래로 */
  animation: fadeSlideDown 0.6s ease forwards;
}

/* 카드별 딜레이 추가 */
.movie-card:nth-child(1) {
  animation-delay: 0.4s;
}

.movie-card:nth-child(2) {
  animation-delay: 0.8s;
}

.movie-card:nth-child(3) {
  animation-delay: 1.2s;
}

/* 애니메이션 키프레임 */
@keyframes fadeSlideDown {
  from {
    opacity: 0;
    transform: translateY(-20px); /* 초기 위치 위로 이동 */
  }
  to {
    opacity: 1;
    transform: translateY(0); /* 원래 위치 */
  }
}
</style>
