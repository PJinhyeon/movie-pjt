<template>
  <div class="article-container" style="margin-top: 3rem;">
    <div class="article-detail">
      <!-- 왼쪽: 포스터 -->
      <div class="poster-section">
        <img
          v-if="article?.movie?.poster_path"
          :src="'https://image.tmdb.org/t/p/w500' + article.movie.poster_path"
          alt="Movie Poster"
          class="poster-image"
        />
      </div>

      <!-- 오른쪽: 게시글 및 댓글 -->
      <div class="content-section">
        <div class="info-container">
          <!-- 게시글 제목 -->
          <h1 class="article-title">{{ article?.title }}</h1>

          <!-- 영화 제목 -->
          <p class="movie-title"><{{ article?.movie?.title }}></p>

          <!-- 게시글 내용 -->
          <p class="article-content">{{ article?.content }}</p>

          <!-- 작성자 정보 -->
          <div class="author-info">
            <img
              :src="article?.user_avatar || defaultProfileImage"
              alt="Author Avatar"
              class="profile-picture-article"
            />
            <div class="author-detail">
              <p class="author-name">{{ article?.user }}</p>
              <small class="created-at">작성일: {{ new Date(article?.created_at).toLocaleDateString() }}</small>
            </div>
          </div>
        </div>

        <!-- 게시글 수정 버튼 -->
        <button v-if="isOwner" @click="goToUpdate" class="edit-button">게시글 수정</button>

        <!-- 댓글 섹션 -->
        <div class="comment-section">
          <h4>댓글</h4>
          <div class="comments-list">
            <div v-for="comment in comments" :key="comment.id" class="comment-container">
              <div class="comment-author">
                <img
                  :src="comment.user_avatar || defaultProfileImage"
                  alt="Comment Author Avatar"
                  class="profile-picture-comment"
                />
                <p class="comment-user">{{ comment.user }}</p>
              </div>
              <p class="comment-content">{{ comment.content }}</p>
              <small class="comment-date">
                작성일: {{ new Date(comment.created_at).toLocaleDateString() }}
              </small>
            </div>
            <div v-if="!comments.length" class="no-comments">댓글이 없습니다. 첫 댓글을 작성해보세요!</div>
          </div>

          <!-- 댓글 입력 상자 및 버튼 -->
          <div class="comment-input-container">
            <textarea
              v-model="newComment"
              placeholder="댓글을 입력하세요"
              class="comment-textarea"
            ></textarea>
            <button @click="postComment" class="comment-button">댓글 추가</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { useCounterStore } from '@/stores/counter';
import defaultProfileImage from '@/assets/default-profile.png';

const route = useRoute();
const router = useRouter();
const store = useCounterStore();

const comments = ref([]);
const newComment = ref('');
const article = ref(null);
const articleId = route.params.articleId;
const isOwner = ref(false);


onBeforeUnmount(() => {
  document.body.style.background = '' // 기본 배경으로 복원
});

// 게시글 및 댓글 데이터 로드
onMounted(() => {
  document.body.style.background = '#572200'
  store.fetchLoggedInUserId();

  // 게시글 데이터 로드
  axios
    .get(`http://127.0.0.1:8000/community/articles/${articleId}/`)
    .then((res) => {
      article.value = res.data;
      checkOwner(); // 게시글 데이터 로드 후 소유자 확인
    })
    .catch((err) => {
      console.error('게시글 데이터를 가져오는 중 에러 발생:', err);
    });

  // 댓글 데이터 로드
  loadComments();
});

// 댓글 데이터 로드 함수
const loadComments = () => {
  axios
    .get(`http://127.0.0.1:8000/community/articles/${articleId}/comments/`)
    .then((res) => {
      comments.value = res.data;
    })
    .catch((err) => {
      console.error('댓글 데이터를 가져오는 중 에러 발생:', err);
    });
};

// 댓글 작성 함수
const postComment = () => {
  if (!newComment.value.trim()) {
    console.error('댓글 내용이 비어 있습니다.');
    return;
  }

  axios
    .post(
      `http://127.0.0.1:8000/community/articles/${articleId}/comments/`,
      { content: newComment.value },
      { headers: { Authorization: `Token ${localStorage.getItem('authToken')}` } }
    )
    .then((res) => {
      comments.value.push(res.data);
      newComment.value = '';
    })
    .catch((err) => {
      console.error('댓글 작성 중 에러 발생:', err);
    });
};

// 작성자와 로그인한 사용자 비교
const checkOwner = () => {
  if (article.value && store.loggedInUser) {
    isOwner.value = article.value.user === store.loggedInUser.username;
    console.log('게시글 소유자:', article.value.user);
    console.log('로그인 사용자:', store.loggedInUser.username);
    console.log('isOwner:', isOwner.value);
  }
};

// 수정 페이지로 이동
const goToUpdate = () => {
  router.push({ name: 'ArticleUpdateView', params: { articleId } });
};
</script>

<style scoped>
/* 전체 컨테이너 스타일 */
.article-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
  background-color: #fff;
  border-radius: 16px; /* 전체 테두리 둥글게 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* 전체 그림자 */
}

/* 내부 레이아웃 */
.article-detail {
  display: flex;
  gap: 24px;
}

/* 포스터 섹션 */
.poster-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.poster-image {
  width: 80%;
  height: auto;
  border-radius: 8px;
  margin-left: 2rem;
  border: 2px solid #572200;
}

/* 콘텐츠 섹션 */
.content-section {
  flex: 2;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 게시글 정보 */
/* info-container 스타일 */
.info-container {
  padding: 0px 24px;
}

/* 게시글 제목 */
.article-title {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 8px; /* 제목과 다른 요소 간격 */
  color: #572200;
}

/* 영화 제목 */
.movie-title {
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 16px;
  color: #874D17;
}

/* 게시글 내용 */
.article-content {
  font-size: 1.2rem;
  line-height: 1.6;
  margin-bottom: 24px;
  color: #874D17
}

/* 작성자 정보 */
.author-info {
  display: flex;
  align-items: center;
  gap: 16px; /* 아바타와 이름 간격 */
}

.author-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
}

.author-detail {
  display: flex;
  flex-direction: column;
}

.author-name {
  font-size: 1rem;
  margin: 0;
  color: #572200;
}

.created-at {
  font-size: 0.8rem;
  color: #777;
}

/* 댓글 섹션 */
h3 {
  margin: 0px;
}

.comment-section {
  padding: 0px 24px;
}

.comments-list {
  max-height: 200px;
  overflow-y: auto;
  margin-bottom: 16px;
}

.comment-container {
  border-bottom: 1px solid #ddd;
  padding: 8px 0;
}

.comment-author {
  display: flex;
  align-items: center;
  gap: 8px;
}

.comment-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
}

.comment-user {
  font-size: 1rem;
}

.comment-content {
  margin: 4px 0;
}

.comment-date {
  font-size: 0.8rem;
  color: #777;
}

/* 댓글 입력 */
.comment-input-container {
  display: flex;
  gap: 8px;
  align-items: center;
}

.comment-textarea {
  flex: 1;
  height: 40px;
  padding: 8px;
  border-radius: 8px;
  border: 1px solid #ddd;
}

.edit-button,
.comment-button {
  background-color: #874d17;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.comment-button:hover {
  background-color: #572200;
}

/* 프로필 이미지 스타일 */
.profile-picture-article {
  width: 40px; /* 작고 동그랗게 설정 */
  height: 40px;
  border-radius: 50%; /* 동그랗게 만들기 */
  object-fit: cover;
  border: 1px solid #ddd; /* 약간의 테두리 */
}

.profile-picture-comment {
  width: 25px; /* 작고 동그랗게 설정 */
  height: 25px;
  border-radius: 50%; /* 동그랗게 만들기 */
  object-fit: cover;
  border: 1px solid #ddd; /* 약간의 테두리 */
}

</style>
