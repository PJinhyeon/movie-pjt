<template>
  <div class="card" @click="goToDetail">
    <!-- 작성일 -->
    <div class="card-date">{{ new Date(article.created_at).toLocaleDateString() }}</div>
    <!-- 영화 포스터 -->
    <img
      v-if="article.movie.poster_path"
      :src="'https://image.tmdb.org/t/p/w200' + article.movie.poster_path"
      alt="Movie Poster"
      class="card-poster"
    />
    <!-- 기사 제목 -->
    <div class="card-title">{{ article.title }}</div>

    <!-- 마우스 오버 시 표시되는 내용 -->
    <div class="card-hover">
      <h2 class="hover-title">{{ article.title }}</h2>
      <p class="hover-author">By {{ article.user }}</p>
      <p class="hover-content">{{ article.content }}</p>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();

const props = defineProps({
  article: {
    type: Object,
    required: true,
  },
});

const goToDetail = () => {
  router.push({ 
    name: 'ArticleDetailView', 
    params: { articleId: props.article.id },
  });
};
</script>

<style scoped>
/* 카드 스타일 */
.card {
  position: relative;
  width: 300px;
  height: 400px;
  background-color: #f7f4ef; /* 연한 아이보리 */
  /* border: 2px solid #BF883C;  */
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  padding: 16px; /* 카드 내부 패딩 추가 */
}

.card:hover {
  transform: translateY(-10px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

/* 작성일 */
.card-date {
  position: absolute;
  top: 20px; /* 상단에서 여백 */
  left: 20px; /* 왼쪽에서 여백 */
  font-size: 0.9rem;
  color: #874d17; /* 진한 갈색 */
  font-weight: bold;
}

/* 영화 포스터 */
.card-poster {
  position: absolute;
  top: 20px; /* 상단 여백 */
  right: 20px; /* 오른쪽 여백 */
  width: 100px;
  object-fit: cover;
}

/* 기사 제목 */
.card-title {
  position: absolute;
  bottom: 20px; /* 하단에서 여백 */
  left: 20px; /* 왼쪽에서 여백 */
  font-size: 1.5rem;
  color: #874d17; /* 진한 갈색 */
  font-weight: bold;
}

/* 마우스 오버 내용 */
.card-hover {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;

  background-color: #572200; /* 어두운 갈색 */
  color: #f7f4ef; /* 연한 아이보리 텍스트 */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center; /* 중앙 정렬 */
  opacity: 0; /* 기본 상태에서 숨김 */
  transition: opacity 0.3s ease, background-color 0.3s ease;
}

.card:hover .card-hover {
  opacity: 1; /* 마우스 오버 시 표시 */
}

/* 마우스 오버 텍스트 스타일 */
.hover-title {
  margin-bottom: 10px;
  font-size: 1.5rem;
  font-weight: bold;
  text-align: center; /* 제목 중앙 정렬 */
}

.hover-author {
  margin-bottom: 10px;
  font-size: 1rem;
  text-align: center; /* 작성자 중앙 정렬 */
  color: #ffe474; /* 밝은 노란색 (강조) */
}

.hover-content {
  font-size: 1rem;
  line-height: 1.5;
  text-align: center; /* 본문 중앙 정렬 */
  margin-top: 10px;
  padding: 30px;
}
</style>