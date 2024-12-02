<template>
  <div class="movie-detail-container" v-if="movie">
    <!-- 장르 이름 배경 텍스트 -->
    <div class="genre-text-container">
      <p
        v-for="genre in movie.genres"
        :key="genre.id"
        class="genre-text"
      >
        {{ genreMap[genre.name] || genre.name }}
      </p>
    </div>

    <!-- 영화 콘텐츠 -->
    <div class="movie-content">
      <!-- 영화 포스터 -->
      <div class="movie-poster">
        <img
          :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path"
          alt="Movie Poster"
          class="poster-image"
        />
      </div>

      <!-- 영화 제목 -->
      <div class="movie-header">
        <h1 class="movie-title">{{ movie.title }}</h1>
      </div>

      <h3>◆</h3>

      <div>
        
        <!-- 영화 설명 -->
        <div class="movie-overview">
          <p class="overview-text">{{ movie.overview }}</p>
        </div>
        
  
        <!-- 영화 세부 정보 -->
        <div class="movie-details">
          <p>개봉일: <span>{{ movie.release_date }}</span></p>
          <p>런타임: <span>{{ movie.runtime }} 분</span></p>
          <p>평균 평점: <span>{{ movie.vote_average }} ({{ movie.vote_count }})</span></p>
        </div>

        


  
        <!-- 출연진 정보 -->
        <div class="movie-cast">
          <h3 class="cast-header">출연진</h3>
          <div class="actor-list">
            <div v-for="actorInfo in actor" :key="actorInfo.name" class="actor-card">
              <img
                :src="actorInfo.profile_path ? 'https://media.themoviedb.org/t/p/w138_and_h175_face' + actorInfo.profile_path : defaultProfileImage"
                alt="Actor Profile"
                class="actor-profile"
              />
              <p class="actor-name">{{ actorInfo.name }}</p>
              <p class="actor-role">as {{ actorInfo.character }}</p>
            </div>
          </div>
        </div>

         <!-- 찜 버튼 -->
    <div class="movie-actions">
      <button
        v-if="isInCart(movie.id)"
        @click="removeFromCart(movie)"
        class="cart-button added"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="white" viewBox="0 0 24 24" width="20" height="20">
          <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
        </svg>
      </button>
      <button
        v-else
        @click="addToCart(movie)"
        class="cart-button"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="#874d17" viewBox="0 0 24 24" width="20" height="20">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 21l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21z"/>
        </svg>
      </button>
    </div>


        <!-- 장르버튼 -->
        <div class="movie-genres">
      <div class="genres-container">
        <button
          v-for="genre in movie.genres"
          :key="genre.id"
          class="genre-button"
          @click="filterByGenre(genre)"
        >
          {{ genre.name }}
        </button>
      </div>
    </div>


      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import axios from "axios";
import { useRoute } from "vue-router";
import defaultProfileImage from "@/assets/default-profile.png";
import { useRouter } from "vue-router";
import { useCartStore } from '@/stores/cart';

const cart = useCartStore();
const router = useRouter()
const route = useRoute();
const movieId = route.params.movie_id;
const movie = ref(null);
const actor = ref([]);

// 장르 이름 매핑
const genreMap = {
  "액션": "ACTION",
  "모험": "ADVENTURE",
  "애니메이션": "ANIMATION",
  "코미디": "COMEDY",
  "범죄": "CRIME",
  "다큐멘터리": "DOCUMENTARY",
  "드라마": "DRAMA",
  "가족": "FAMILY",
  "판타지": "FANTASY",
  "역사": "HISTORY",
  "공포": "HORROR",
  "음악": "MUSIC",
  "미스터리": "MYSTERY",
  "로맨스": "ROMANCE",
  "SF": "SCIENCE FICTION",
  "TV 영화": "TV MOVIE",
  "스릴러": "THRILLER",
  "전쟁": "WAR",
  "서부": "WESTERN",
};

// 데이터 로드 및 body 배경색 변경
onMounted(() => {
  document.body.style.background = "#572200"; // 진한 갈색 배경으로 변경

  // 영화 정보 가져오기
  axios.get(`http://127.0.0.1:8000/movies/${movieId}/`).then((res) => {
    movie.value = res.data;
  });

  // 출연진 정보 가져오기
  axios.get(`http://127.0.0.1:8000/movies/${movieId}/credits/`).then((res) => {
    actor.value = res.data.cast.slice(0, 9).map((person) => ({
      name: person.name,
      character: person.character,
      profile_path: person.profile_path,
    }));
  });
});
const isInCart = (movieId) => {
  return cart.cartItems.some((item) => item.movie === movieId);
};


// 페이지 떠날 때 body 배경 복원
onUnmounted(() => {
  document.body.style.background = ""; // 원래 배경으로 복원
});

const filterByGenre = (genre) => {
  router.push({
    name: 'GenreFilteredMovies',
    params: { genreId: genre.id },
  });
};

const removeFromCart = function (movie) {
  cart.removeCart(movie.id);
};

const addToCart = function (movie) {
  cart.addCart(movie.id);
  console.log(cart.cartItems);
};




</script>

<style scoped>
/* 전체 컨테이너 */
.movie-detail-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  position: relative;
  width: 100%;
  height: 100%;
  color: #ffe474;
  overflow: hidden;
}

/* 장르 텍스트 배경 */
.genre-text-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 70%; /* 포스터 영역 */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: -1;
}

.genre-text {
  font-size: 14rem; /* 매우 큰 텍스트 */
  font-weight: bold;
  color: rgba(255, 228, 116, 0.3); /* 투명도를 준 노란색 */
  text-transform: uppercase;
  text-align: center;
  line-height: 1.2;
  margin: 0;
  white-space: nowrap;
}

/* 영화 콘텐츠 */
.movie-content {
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 90%;
  max-width: 800px;
  margin-top: 5rem;
}

/* 영화 포스터 */
.movie-poster {
  margin-bottom: 20px;
}

.poster-image {
  width: 100%;
  max-width: 500px;
  aspect-ratio: 2 / 3;
  border-radius: 16px;
  object-fit: cover;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.8);
  animation: fade-in 1s ease-in-out; /* 포스터 로딩 효과 */
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* 영화 제목 */
.movie-header {
  margin: 1rem 0;
  text-align: center;
  width: 100%;
  background: linear-gradient(90deg, #FFE474, #874D17); /* 왼쪽에서 오른쪽으로 그라데이션 */
  padding: 1rem 0; /* 상하 여백 추가 */
  color: #572200; /* 텍스트 색상 조정 */
}


.movie-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #572200;
}


/* 영화 설명 */
.movie-overview {
  margin: 1rem 0;
  text-align: center;
}

.overview-text {
  font-size: 1.2rem;
  line-height: 1.8;
  color: #e5ba5e;
}

.movie-details {
  margin: 1rem 0;
  padding: 3rem;
}


.movie-details p {
  font-size: 1.1rem;
  color: #e5ba5e;
}

.movie-details span {
  font-weight: bold;
  color: #ffe474;
}

/* 출연진 정보 */
.movie-cast {
  margin: 30px 0;
  text-align: center;
}

.cast-header {
  font-size: rem;
  color: #ffe474;
}

.actor-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.actor-card {
  width: 120px;
  text-align: center;
}

.actor-profile {
  width: 100%;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 10px;
  border: 2px solid #ffe474;
}

.actor-name {
  font-size: 1rem;
  font-weight: bold;
  color: #ffe474;
}

.actor-role {
  font-size: 0.85rem;
  color: #e5ba5e;
}

.movie-genres {
  margin-bottom: 20px;
}
.genres-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}
.genre-button {
  flex: 1 1 auto;
  max-width: 150px; /* 버튼 크기를 조금 더 키움 */
  text-align: center;
  padding: 10px 14px;
  background-color: #ffe474; /* 동일한 노란색 */
  color: #572200;
  border: 1px solid #874d17; /* 외곽선으로 포인트 */
  border-radius: 10px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.genre-button:hover {
  background-color: #874d17; /* 호버 시 갈색으로 변경 */
  color: #fff; /* 텍스트 색상을 흰색으로 변경 */
  transform: translateY(-3px); /* 약간 위로 이동 효과 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 버튼에 그림자 추가 */
}

/* 찜 버튼 */
.movie-actions {
  margin-top: 20px;
  margin-bottom: 40px;
  display: flex;
  justify-content: center;
  gap: 10px;
}

.cart-button {
  padding: 10px 20px;
  background-color: #ffe474; /* 기존 색상과 조화로운 노란색 */
  color: #572200; /* 텍스트 색상은 갈색으로 통일 */
  border: none;
  border-radius: 10px; /* 약간 둥근 모서리 */
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease; /* 부드러운 전환 효과 */
  display: flex;
  align-items: center;
  justify-content: center;
}

.cart-button svg {
  margin-right: 8px; /* 아이콘과 텍스트 간 간격 */
}

.cart-button.added {
  background-color: #874d17; /* 찜한 경우 어두운 갈색 */
  color: #fff;
}

.cart-button:hover {
  transform: scale(1.05); /* 살짝 확대 효과 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 버튼에 그림자 추가 */
}


</style>
