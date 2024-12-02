<template>
  <div class="community-container">
    <!-- 헤더 -->
    <header class="community-header">
      <h1>커뮤니티</h1>
      <input
        type="text"
        v-model="searchQuery"
        @input="searchArticles"
        class="search-input"
        placeholder="게시글 검색"
      />
    </header>

    <!-- 검색 결과 -->
    <section v-if="isSearching" class="search-results">
      <h2>검색 결과</h2>
      <div v-if="searchResults.length">
        <div v-for="article in searchResults" :key="article.id" class="search-card">
          <h3>{{ article.movie.title }}</h3>
          <p>{{ article.content }}</p>
        </div>
      </div>
      <p v-else>검색어 "{{ searchQuery }}"에 대한 결과가 없습니다.</p>
    </section>

    <!-- 게시글 섹션 -->
    <section v-else>
      <!-- 댓글 많은 게시글 -->
      <div class="section">
        <h2>댓글 많은 게시글</h2>
        <!-- 슬라이더 버튼 추가 -->
        <button 
          class="slider-button left" 
          @click="scrollLeft" 
          :disabled="scrollPosition === 0"
        >‹</button>
        
        <div class="top-commented-list-container">
          <div
            class="top-commented-list"
            :style="{ transform: `translateX(-${scrollPosition * (220 + 16)}px)` }"
          >
            <ArticleCard
              v-for="article in topCommented.slice(0, 10)" 
              :key="article.id"
              :article="article"
              :layout="'compact'"
            />
          </div>
        </div>

        <button 
          class="slider-button right" 
          @click="scrollRight" 
          :disabled="scrollPosition + articlesPerView >= maxArticles"
        >›</button>
      </div>

      <!-- 최신 게시글 -->
      <div class="section">
        <h2>최신 게시글</h2>
        <div class="recent-list">
          <div v-for="article in recentArticles" :key="article.id" class="recent-list-item">
          <RecentArticle :article="article" />
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import axios from 'axios';
import ArticleCard from '@/components/ArticleCard.vue';
import RecentArticle from '@/components/RecentArticle.vue';

const searchQuery = ref('');
const topCommented = ref([]);
const recentArticles = ref([]);
const searchResults = ref([]);
const isSearching = ref(false);

const scrollPosition = ref(0); // 현재 슬라이더 위치
const articlesPerView = ref(3); // 한 번에 표시할 게시글 수
const maxArticles = 5; // 최대 게시글 수

// 검색 기능
const searchArticles = () => {
  isSearching.value = searchQuery.value.trim() !== '';
  if (isSearching.value) {
    axios
      .get(`http://127.0.0.1:8000/community/articles/search/?q=${searchQuery.value}`)
      .then((res) => {
        searchResults.value = res.data;
      })
      .catch((err) => console.error(err));
  } else {
    searchResults.value = [];
  }
};

// 게시글 불러오기
const fetchArticles = () => {
  axios
    .get('http://127.0.0.1:8000/community/main/')
    .then((res) => {
      topCommented.value = res.data.top_commented;
      recentArticles.value = res.data.recent;
    })
    .catch((err) => console.error(err));
};

// 화면 크기에 따라 articlesPerView 계산
const calculateArticlesPerView = () => {
  const containerWidth = window.innerWidth;
  if (containerWidth > 1200) {
    articlesPerView.value = 3;
  } else if (containerWidth > 800) {
    articlesPerView.value = 2;
  } else {
    articlesPerView.value = 1;
  }
};

// 슬라이더 동작
const scrollLeft = () => {
  scrollPosition.value = Math.max(scrollPosition.value - 1, 0); // 왼쪽으로 한 칸 이동
};

const scrollRight = () => {
  const maxScroll = Math.max(maxArticles - articlesPerView.value, 0); // 최대 이동 가능 범위
  scrollPosition.value = Math.min(scrollPosition.value + 1, maxScroll); // 오른쪽으로 한 칸 이동
};

onMounted(() => {
  document.body.style.background = '#572200'
  fetchArticles();
  calculateArticlesPerView();
  window.addEventListener('resize', calculateArticlesPerView);
  console.log("Background:", getComputedStyle(document.body).background)

});

onBeforeUnmount(() => {
  document.body.style.background = '' // 기본 배경으로 복원
  window.removeEventListener('resize', calculateArticlesPerView);
});
</script>

<style scoped>
.community-header {
  text-align: center;
  margin-bottom: 20px;
}

.community-header h1 {
  font-size: 2rem;
  color: #FFE474;
}

.search-input {
  width: 100%;
  max-width: 400px;
  padding: 10px;
  border: 2px solid #572200;
  border-radius: 8px;
  font-size: 1rem;
  outline: none;
}

.section {
  width: 100%;
  margin-bottom: 40px;
  position: relative;
}

/* 댓글 많은 게시글 */
.top-commented-list-container {
  display: flex;
  align-items: center;
  overflow: hidden;
  width: 100%;
  height: 320px;
}

.top-commented-list {
  display: flex;
  transition: transform 0.5s ease-in-out;
}

.top-commented-list > * {
  flex-shrink: 0;
  width: 220px;
  height: 300px;
  margin-right: 16px;
}

/* 슬라이더 버튼 */
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
  height: 60px;
  width: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.slider-button.left {
  left: -20px;
}

.slider-button.right {
  right: -20px;
}

.slider-button:disabled {
  background-color: rgba(0, 0, 0, 0.2);
  cursor: not-allowed;
}

/* 최신 게시글 */
.recent-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.recent-list-item {
  /* background-color: white; */
  width: 80%; /* 너비 축소 */
  margin: 0 auto; /* 가운데 정렬 */
  border-radius: 8px;
  padding: 16px;
  /* box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); */
}

/* 가로선 애니메이션 */
@keyframes draw-line {
  from {
    width: 0%;
  }
  to {
    width: 100%;
  }
}
</style>
