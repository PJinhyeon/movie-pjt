<template>
  <div class="movie-list-wrapper">
    <!-- 왼쪽 버튼 -->
    <button 
      class="slider-button left" 
      @click="scrollLeft" 
      :disabled="scrollPosition === 0"
    >‹</button>
    
    <!-- 영화 리스트 슬라이더 -->
    <div class="movie-list-container">
      <div 
        class="movie-items"
        :style="{ transform: `translateX(-${scrollPosition * (200 + 20)}px)` }"
      >
        <div 
          v-for="(movie, index) in visibleMovies" 
          :key="movie.id" 
          class="movie-item"
        >
          <!-- 순위는 고정된 값으로 계산 -->
          <span class="movie-rank">{{ index + 1 }}</span>
          <MovieCard 
            :movie="movie" @click.prevent="onClick(movie)"
          />
        </div>
      </div>
    </div>
    
    <!-- 오른쪽 버튼 -->
    <button 
      class="slider-button right" 
      @click="scrollRight" 
      :disabled="scrollPosition + moviesPerView >= maxMovies"
    >›</button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useCounterStore } from '@/stores/counter'; // Pinia 스토어
import MovieCard from '@/components/MovieCard.vue'; // 영화 카드 컴포넌트
import { useRouter } from 'vue-router';
const router = useRouter()
const store = useCounterStore();
const scrollPosition = ref(0); // 현재 스크롤 위치
const moviesPerView = ref(5); // 한 번에 표시할 영화 수 (동적으로 변경)
const maxMovies = 10; // 최대 표시할 영화 수 (10위까지만)

// 10위까지만 표시
const visibleMovies = computed(() => {
  return store.popular_movies.slice(0, maxMovies); // 10위까지만 가져오기
});

// 화면 크기에 따라 moviesPerView 계산
function calculateMoviesPerView() {
  const containerWidth = window.innerWidth;
  if (containerWidth > 1200) {
    moviesPerView.value = 5;
  } else if (containerWidth > 800) {
    moviesPerView.value = 3;
  } else {
    moviesPerView.value = 2;
  }
}

// 초기화 및 화면 크기 변경 이벤트 설정
onMounted(() => {
  store.getMovies();
  calculateMoviesPerView();
  window.addEventListener('resize', calculateMoviesPerView);
});

onUnmounted(() => {
  window.removeEventListener('resize', calculateMoviesPerView);
});

// 슬라이더 동작
function scrollLeft() {
  scrollPosition.value = Math.max(scrollPosition.value - 1, 0); // 한 칸씩 이동
}

function scrollRight() {
  const maxScroll = Math.max(maxMovies - moviesPerView.value, 0); // 10위까지만 스크롤 허용
  scrollPosition.value = Math.min(scrollPosition.value + 1, maxScroll); // 한 칸씩 이동
}
const onClick = (movie) => {
  router.push({
    name: 'MovieDetailView',
    params: { movie_id: movie.id },
  })
}
</script>

<style scoped>
.movie-list-wrapper {
  display: flex;
  align-items: center;
  position: relative;
  justify-content: center; /* 영화 리스트를 중간에 정렬 */
}

.movie-list-container {
  display: flex;
  overflow: hidden; /* 스크롤 바를 숨깁니다 */
  width: 80%; /* 중앙 정렬을 위한 고정 너비 */
  position: relative;
}

.movie-items {
  display: flex;
  transition: transform 0.5s ease-in-out; /* 애니메이션 효과 추가 */
}

.movie-item {
  flex: 0 0 auto;
  width: 200px;
  height: 300px;
  margin-right: 20px;
  position: relative;
}

.movie-rank {
  position: absolute;
  top: 10px;
  left: 10px;
  font-size: 3rem;
  font-weight: bold;
  color: rgba(255, 255, 255, 0.8);
  z-index: 1;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
}

.slider-button {
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  padding: 10px;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
}

.slider-button.left {
  left: 0;
}

.slider-button.right {
  right: 0;
}

.slider-button:disabled {
  background-color: rgba(0, 0, 0, 0.2);
  cursor: not-allowed;
}


</style>
