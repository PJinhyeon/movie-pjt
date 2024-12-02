<template>
  <div class="search-view-container">
    <!-- 제목 -->
    <h1 class="search-header">Search for a Movie</h1>

    <!-- 검색창 -->
    <div class="search-input-container">
      <input
        type="text"
        v-model="searchQuery"
        @input="searchMovies"
        placeholder="Type a movie name..."
        class="search-input"
      />
    </div>

    <!-- 검색 결과 -->
    <div v-if="movies.length" class="movie-results-section">
      <h2 class="section-header">Search Results</h2>
      <div class="movie-list">
        <MovieCard
          v-for="movie in movies"
          :key="movie.id"
          :movie="movie"
          @click="saveSearchHistory(movie.title, movie)"
        />
      </div>
    </div>

    <!-- 검색 결과가 없을 때 -->
    <div v-else-if="searchQuery.trim() !== ''" class="no-results-section">
      <p>No results found for "{{ searchQuery }}".</p>
    </div>

    <!-- 초기 화면 -->
    <div v-else class="initial-section">
      <p>Start searching for a movie above.</p>
    </div>

    <!-- 검색 기록 섹션 -->
    <div v-if="searchHistories.length" class="search-history-section">
  <h2 class="section-header">Search History</h2>
  <ul class="history-list">
    <li v-for="history in searchHistories" :key="history.id" class="history-item">
      <p>{{ history.keyword }}</p>
    </li>
  </ul>
  <button @click="deleteSearchHistories" class="clear-history-button">
    Clear Search History
  </button>
</div>

  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import MovieCard from '@/components/MovieCard.vue';
import { useRouter } from 'vue-router';
import { useCounterStore } from '@/stores/counter';

const router = useRouter();
const searchQuery = ref(''); // 검색어
const movies = ref([]); // 검색 결과
const searchHistories = ref([]); // 검색 기록 데이터
const store = useCounterStore();
const token = localStorage.getItem('authToken'); // 인증 토큰
const apiUrl = 'http://127.0.0.1:8000/search-history/'; // API 엔드포인트

// 영화 검색 메서드
const searchMovies = () => {
  const query = searchQuery.value.trim();
  if (query === '') {
    movies.value = [];
    return;
  }

  axios
    .get(`http://127.0.0.1:8000/movies/search/?query=${query}`)
    .then((res) => {
      movies.value = res.data.results; // TMDB API의 영화 데이터
    })
    .catch((err) => {
      console.error('Error searching movies:', err);
      movies.value = [];
    });
};

// 검색 기록 가져오기
const fetchSearchHistories = () => {
  if (store.isLogin) {
    axios({
      method: 'get',
      url: apiUrl,
      headers: {
        Authorization: `Token ${token}`,
      },
    })
      .then((res) => {
        searchHistories.value = res.data; // 검색 기록 업데이트
      })
      .catch((err) => {
        console.error('Error fetching search histories:', err);
      });
  }
};

// 검색 기록 저장
const saveSearchHistory = (keyword, movie) => {
  if (store.isLogin) {
    axios({
      method: 'post',
      url: apiUrl,
      headers: {
        Authorization: `Token ${token}`,
      },
      data: {
        keyword: keyword, // 영화 제목
        movie: movie.id,  // 영화 ID
      },
    })
      .then((res) => {
        searchHistories.value.push(res.data);
        router.push({
          name: 'MovieDetailView',
          params: { movie_id: movie.id },
        });
      })
      .catch((err) => {
        console.error('Error saving search history:', err);
      });
  } else{
    router.push({
          name: 'MovieDetailView',
          params: { movie_id: movie.id },
        });
  }
};

// 검색 기록 삭제
const deleteSearchHistories = () => {
  axios({
    method: 'delete',
    url: `${apiUrl}delete/`,
    headers: {
      Authorization: `Token ${token}`,
    },
  })
    .then(() => {
      searchHistories.value = [];
    })
    .catch((err) => {
      console.error('Error deleting search histories:', err);
    });
};

// 초기 로드 시 검색 기록 가져오기
fetchSearchHistories();
</script>


<style scoped>
/* 전체 컨테이너 */
.search-view-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

/* 제목 */
.search-header {
  text-align: center;
  font-size: 2rem;
  color: #572200;
  margin-bottom: 20px;
}

/* 검색창 */
.search-input-container {
  text-align: center;
  margin-bottom: 20px;
}

.search-input {
  width: 100%;
  max-width: 500px;
  padding: 10px 15px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-input:focus {
  outline: none;
  border-color: #874d17;
  box-shadow: 0 0 6px rgba(135, 77, 23, 0.4);
}

/* 검색 결과 */
.movie-results-section {
  margin-bottom: 20px;
}

.section-header {
  font-size: 1.5rem;
  color: #FFE474;
  margin-bottom: 10px;
}

/* 검색 기록 */
.search-history-section {
  margin-top: 30px;
}

.history-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.history-item {
  padding: 8px 0;
  border-bottom: 1px solid #ddd;
  font-size: 0.95rem;
  color: #572200;
}

.clear-history-button {
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #874d17;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.clear-history-button:hover {
  background-color: #572200;
}

/* 영화 목록 */
.movie-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: center;
}

/* 검색 결과가 없을 때 */
.no-results-section,
.initial-section {
  text-align: center;
  font-size: 1rem;
  color: #572200;
}
</style>
