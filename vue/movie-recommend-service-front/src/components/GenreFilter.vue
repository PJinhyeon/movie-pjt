<template>
  <div style="margin-top: 30px;">
    <!-- 슬라이더 섹션 -->
    <div class="genre-slider-container">
      <div class="genre-slider-track">
        <!-- "전체" 카드 -->
        <div 
          class="genre-card" 
          :class="{ active: selectedGenre === 'all' }" 
          @click="selectGenre('all')"
        >
        <img :src="allImage" alt="전체" class="genre-image" />
          <div class="genre-content">
            <!-- <p class="genre-subtitle">Album</p> -->
            <h3 class="genre-title">전체</h3>
            <span class="genre-arrow">→</span>
          </div>
        </div>

        <!-- 장르 카드들 -->
        <div 
          v-for="(genre, index) in genres" 
          :key="'card1-' + genre.id" 
          class="genre-card"
          :class="{ active: selectedGenre === genre.id }"
          @click="selectGenre(genre.id)"
        >
        <img :src="getGenreImage(genre.id)" :alt="genre.name" class="genre-image" />
          <div class="genre-content">
            <!-- <p class="genre-subtitle">Album</p> -->
            <h3 class="genre-title">{{ genre.name }}</h3>
            <span class="genre-arrow">→</span>
          </div>
        </div>

        <!-- 복제된 "전체" 카드 (무한 루프용) -->
        <div 
          class="genre-card" 
          :class="{ active: selectedGenre === 'all' }" 
          @click="selectGenre('all')"
        >
        <img :src="allImage" alt="전체" class="genre-image" />
          <div class="genre-content">
            <!-- <p class="genre-subtitle">Album</p> -->
            <h3 class="genre-title">전체</h3>
            <span class="genre-arrow">→</span>
          </div>
        </div>

        <!-- 복제된 장르 카드들 (무한 루프용) -->
        <div 
          v-for="(genre, index) in genres" 
          :key="'card2-' + genre.id" 
          class="genre-card"
          :class="{ active: selectedGenre === genre.id }"
          @click="selectGenre(genre.id)"
        >
        <img :src="getGenreImage(genre.id)" :alt="genre.name" class="genre-image" />
          <div class="genre-content">
            <!-- <p class="genre-subtitle">Album</p> -->
            <h3 class="genre-title">{{ genre.name }}</h3>
            <span class="genre-arrow">→</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineEmits } from 'vue'
import axios from 'axios'
import allImage from '@/assets/genrePic/all.jpg'

// 장르 목록과 선택된 장르
const genres = ref(null)
const selectedGenre = ref('all') 

// 이미지 경로 생성 함수
const getGenreImage = (genreId) => {
  try {
    return new URL(`../assets/genrePic/${genreId}.jpg`, import.meta.url).href
  } catch (e) {
    console.error(`이미지 로드 실패: ${genreId}.jpg`, e)
    return 'https://via.placeholder.com/150' // 기본 이미지
  }
}

// 데이터 로드
onMounted(() => {
  axios({
    method: 'get',
    url: 'http://127.0.0.1:8000/movies/genres/'
  })
    .then((res) => {
      genres.value = res.data.genres
    })
    .catch((err) => {
      console.log('에러: ', err)
    })
})

// 선택된 장르를 업데이트하고 이벤트 발생
const emit = defineEmits(['genreSelected'])
const selectGenre = (genreId) => {
  selectedGenre.value = genreId 
  emit('genreSelected', genreId)
}
</script>


<style scoped>
/* 슬라이더 컨테이너 */
.genre-slider-container {
  overflow: hidden;
  position: relative;
  width: 100%;
  padding: 20px 0;
}

/* 슬라이더 트랙 */
.genre-slider-track {
  display: flex;
  animation: scroll 50s linear infinite; /* 무한 슬라이더 */
  gap: 20px;
}

/* 카드 */
.genre-card {
  flex: 0 0 auto;
  width: 200px;
  height: 300px;
  background-color: #fff;
  border-radius: 16px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.genre-card:hover {
  transform: scale(1.03);
  box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
}

/* 이미지 */
.genre-image {
  width: 120px;
  height: 120px;
  border-radius: 12px;
  object-fit: cover;
}

.genre-content {
  display: flex;
  flex-direction: column;
}

.genre-subtitle {
  font-size: 0.8rem;
  color: #999;
  margin-bottom: 4px;
}

.genre-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #572200;
}

.genre-arrow {
  font-size: 1.5rem;
  color: #874D17;
}

/* 활성화된 카드 */
.genre-card.active {
  background: linear-gradient(90deg, #FFE474, #FFD27D);
  color: #572200;
  font-weight: 900;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  border: 2px solid #FFD27D;
}

/* 무한 스크롤 애니메이션 */
@keyframes scroll {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-100%);
  }
}
</style>
