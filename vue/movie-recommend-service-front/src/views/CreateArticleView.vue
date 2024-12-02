<template>
  <div class="create-post-container">
    <!-- 헤더 -->
    <header class="post-header">
      <h1>게시글 작성</h1>
    </header>

    <!-- 영화 검색 -->
    <div class="search-section">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="영화를 검색하세요"
        @input="searchMovies"
        class="search-input"
      />
      <ul v-if="movies.length" class="search-results">
        <li
          v-for="movie in movies"
          :key="movie.id"
          class="search-item"
          @click="selectMovie(movie)"
        >
          <img
            :src="'https://image.tmdb.org/t/p/w200' + movie.poster_path"
            alt="Movie Poster"
            class="movie-poster"
          />
          <span>{{ movie.title }}</span>
        </li>
      </ul>
    </div>

    <!-- 선택된 영화 -->
    <div v-if="selectedMovie" class="selected-movie">
      <h3>선택된 영화:</h3>
      <p>{{ selectedMovie.title }}</p>
      <img
        :src="'https://image.tmdb.org/t/p/w200' + selectedMovie.poster_path"
        alt="Selected Movie Poster"
        class="selected-poster"
      />
    </div>

    <!-- 게시글 작성 -->
    <div class="post-section">
      <textarea
        v-model="title"
        class="post-title"
        placeholder="게시글 제목을 입력하세요"
      ></textarea>
      <textarea
        v-model="content"
        class="post-content"
        placeholder="게시글 내용을 입력하세요"
      ></textarea>
      <button class="submit-button" @click="createPost">게시글 작성</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      title: "",
      searchQuery: "", // 영화 검색어
      movies: [], // 검색된 영화 목록
      selectedMovie: null, // 선택된 영화 정보
      content: "", // 게시글 내용
    };
  },
  methods: {
    // 영화 검색
    searchMovies() {
      if (this.searchQuery.trim() !== "") {
        axios
          .get(`http://127.0.0.1:8000/movies/search/?query=${this.searchQuery}`)
          .then((res) => {
            this.movies = res.data.results;
          })
          .catch((err) => console.error(err));
      } else {
        this.movies = [];
      }
    },
    // 영화 선택
    selectMovie(movie) {
      this.selectedMovie = movie;
      this.movies = []; // 검색 결과 초기화
    },
    // 게시글 작성
    createPost() {
      if (!this.selectedMovie || !this.content.trim()) {
        alert("영화를 선택하고 게시글 내용을 입력하세요.");
        return;
      }

      axios
        .post(
          "http://127.0.0.1:8000/community/articles/",
          {
            movie_id: this.selectedMovie.id, // 선택된 영화 ID
            title: this.title,
            content: this.content, // 게시글 내용
          },
          {
            headers: {
              Authorization: `Token ${localStorage.getItem("authToken")}`,
            },
          }
        )
        .then((res) => {
          console.log("게시글 작성 성공!", res.data);
          this.$router.push("/community"); // 커뮤니티 페이지로 이동
        })
        .catch((err) => {
          console.error("게시글 작성 실패:", err.response);
          if (err.response && err.response.data) {
            alert(`오류: ${err.response.data.error || "게시글 작성 실패"}`);
          }
        });
    },
  },
};
</script>

<style scoped>
/* 전체 컨테이너 */
.create-post-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
  background-color: #f7f4ef; /* 연한 아이보리 */
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* 외곽 그림자 */
}

/* 헤더 */
.post-header {
  text-align: center;
  margin-bottom: 24px;
}

.post-header h1 {
  font-size: 2rem;
  color: #874d17; /* 진한 갈색 */
}

/* 검색 섹션 */
.search-section {
  margin-bottom: 24px;
  text-align: center; /* 중앙 정렬 */
}

.search-input {
  width: 600px; /* 적절한 너비로 조정 */
  padding: 12px;
  font-size: 1rem;
  border: 2px solid #bf883c;
  border-radius: 8px;
  outline: none;
}

.search-results {
  margin-top: 12px;
  list-style: none;
  padding: 0;
}

.search-item {
  display: flex;
  align-items: center;
  padding: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.search-item:hover {
  background-color: #f5e9db;
}

.movie-poster {
  width: 50px;
  height: 75px;
  margin-right: 12px;
  border-radius: 4px;
  object-fit: cover;
}

/* 선택된 영화 */
.selected-movie {
  margin-bottom: 24px;
  text-align: center;
}

.selected-movie img {
  border-radius: 8px;
  margin-top: 8px;
  width: 120px;
}

/* 게시글 작성 */
.post-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-items: center; /* 중앙 정렬 */
}

.post-title,
.post-content {
  width: 600px; /* 제목과 내용의 너비를 동일하게 설정 */
  padding: 12px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: none;
}

.post-title {
  height: 50px;
}

.post-content {
  min-height: 150px;
}

.submit-button {
  width: 600px; /* 버튼 너비를 입력 필드와 동일하게 설정 */
  background-color: #874d17;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.submit-button:hover {
  background-color: #572200;
}
</style>
