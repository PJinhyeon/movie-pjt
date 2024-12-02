<template>
  <div class="edit-article-container">
    <!-- 헤더 -->
    <header class="edit-header">
      <h1>게시글 수정</h1>
    </header>

    <!-- 게시글 제목 수정 -->
    <div class="form-group">
      <label for="title" class="form-label">제목</label>
      <textarea
        id="title"
        v-model="updatedTitle"
        class="form-title"
        placeholder="게시글 제목을 입력하세요"
      ></textarea>
    </div>

    <!-- 게시글 내용 수정 -->
    <div class="form-group">
      <label for="content" class="form-label">내용</label>
      <textarea
        id="content"
        v-model="updatedContent"
        class="form-content"
        placeholder="게시글 내용을 입력하세요"
      ></textarea>
    </div>

    <!-- 영화 정보 (수정 불가) -->
    <div v-if="article && article.movie" class="movie-info">
      <p class="movie-title">{{ article.movie.title }}</p>
      <img
        v-if="article.movie.poster_path"
        :src="'https://image.tmdb.org/t/p/w200' + article.movie.poster_path"
        alt="Movie Poster"
        class="movie-poster"
      />
    </div>

    <!-- 저장 및 삭제 버튼 -->
    <div class="button-group">
      <button @click="updateArticle" class="save-button">저장</button>
      <button @click="deleteArticle" class="delete-button">삭제</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";

const route = useRoute();
const router = useRouter();
const articleId = route.params.articleId;

// 수정할 게시글 데이터를 저장
const updatedTitle = ref("");
const updatedContent = ref("");
const article = ref(null);

// 게시글 로드
onMounted(() => {
  axios
    .get(`http://127.0.0.1:8000/community/articles/${articleId}/`)
    .then((res) => {
      article.value = res.data;
      updatedTitle.value = res.data.title; // 기존 제목 설정
      updatedContent.value = res.data.content; // 기존 내용 설정
    })
    .catch((err) => {
      console.error("게시글 데이터를 가져오는 중 에러 발생:", err);
    });
});

// 게시글 수정
const updateArticle = () => {
  axios
    .put(
      `http://127.0.0.1:8000/community/articles/${articleId}/`,
      {
        title: updatedTitle.value,
        content: updatedContent.value,
      },
      {
        headers: { Authorization: `Token ${localStorage.getItem("authToken")}` },
      }
    )
    .then(() => {
      alert("게시글이 수정되었습니다.");
      router.push(`/articles/${articleId}`); // 수정 후 게시글 상세 페이지로 이동
    })
    .catch((err) => {
      console.error("게시글 수정 중 에러 발생:", err);
    });
};

// 게시글 삭제
const deleteArticle = () => {
  if (confirm("정말 이 게시글을 삭제하시겠습니까?")) {
    axios
      .delete(`http://127.0.0.1:8000/community/articles/${articleId}/`, {
        headers: { Authorization: `Token ${localStorage.getItem("authToken")}` },
      })
      .then(() => {
        alert("게시글이 삭제되었습니다.");
        router.push("/community"); // 삭제 후 커뮤니티 페이지로 이동
      })
      .catch((err) => {
        console.error("게시글 삭제 중 에러 발생:", err);
      });
  }
};
</script>

<style scoped>
/* 전체 컨테이너 */
.edit-article-container {
  max-width: 800px; /* 중앙 정렬을 위해 너비 제한 */
  margin: 0 auto; /* 가로 중앙 정렬 */
  padding: 24px;
  background-color: #f7f4ef; /* 연한 아이보리 */
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* 외곽 그림자 */
  display: flex; /* 중앙 배치를 위해 flexbox 적용 */
  flex-direction: column;
  align-items: center; /* 세로 중앙 정렬 */
}

/* 헤더 */
.edit-header {
  text-align: center;
  margin-bottom: 24px;
}

.edit-header h1 {
  font-size: 2rem;
  color: #874d17; /* 진한 갈색 */
}

/* 폼 그룹 */
.form-group {
  margin-bottom: 24px;
  width: 100%;
  max-width: 600px; /* 폼 그룹의 너비 제한 */
}

.form-label {
  display: block;
  font-size: 1rem;
  color: #572200; /* 어두운 갈색 */
  margin-bottom: 8px;
  text-align: left;
}

.form-title,
.form-content {
  width: 100%;
  padding: 12px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: none;
}

.form-title {
  height: 50px; /* 제목 입력칸 높이 */
}

.form-content {
  min-height: 150px; /* 내용 입력칸 높이 */
}

/* 영화 정보 */
.movie-info {
  text-align: center;
  margin-bottom: 24px;
}

.movie-title {
  font-weight: bold;
  font-size: 18px;
}

.movie-poster {
  border-radius: 8px;
  margin-top: 8px;
}

/* 버튼 그룹 */
.button-group {
  display: flex;
  justify-content: center;
  gap: 16px;
}

.save-button,
.delete-button {
  width: 150px;
  padding: 12px;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.save-button {
  background-color: #874d17; /* 진한 갈색 */
  color: white;
}

.save-button:hover {
  background-color: #572200;
}

.delete-button {
  background-color: #ff4d4f; /* 빨간색 */
  color: white;
}

.delete-button:hover {
  background-color: #ff7875;
}
</style>
