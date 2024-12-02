<template>
  <div class="mypage-container">
    <!-- 프로필 섹션 -->
    <div class="profile-section">
      <div class="profile-info">
        <img
          :src="user.profile_picture || defaultProfileImage"
          alt="Profile Picture"
          class="profile-picture"
        />
        <div class="profile-details">
          <h2>{{ user.username }}</h2>
          <p>이메일: {{ user.email }}</p>
          <div class="profile-actions" v-if="isOwnProfile">
            <button @click="editProfile" class="edit-button">프로필 수정</button>
            <button @click="goToCreateArticle" class="create-button">글 작성</button>
            <button @click="goToChange" class="change-button">비밀번호 변경</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 탭 섹션 -->
    <div class="tabs-section">
      <button :class="{ active: activeTab === 'articles' }" @click="activeTab = 'articles'">
        내가 작성한 게시물
      </button>
      <button :class="{ active: activeTab === 'wishlist' }" @click="activeTab = 'wishlist'">
        찜 목록
      </button>
      <button :class="{ active: activeTab === 'recommendations' }" @click="activeTab = 'recommendations'">
        추천 받은 영화
      </button>
    </div>

    <!-- 콘텐츠 섹션 -->
    <div class="content-section">
      <div v-if="activeTab === 'articles'">
        <ArticleMyPage />
      </div>
      <div v-if="activeTab === 'wishlist'" class="cart-item-list">
        <CartItem 
          v-if="token"
          v-for="cartItem in cart.cartItems" 
          :key="cartItem.id" 
          :cartItem="cartItem" 
        />
      </div>
      <div v-if="activeTab === 'recommendations'">
        <!-- <p>추천 받은 영화 목록은 여기에 추가됩니다. (추후 구현)</p> -->
        <RecommendedMovies />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onBeforeUnmount } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useCounterStore } from '@/stores/counter';
import axios from 'axios';
import ArticleMyPage from '@/components/ArticleMyPage.vue';
import defaultProfileImage from '@/assets/default-profile.png';
import CartItem from '@/components/CartItem.vue';
import { useCartStore } from '@/stores/cart';
import RecommendedMovies from '@/components/RecommendedMovies.vue';


const cart = useCartStore()
const token = ref(localStorage.getItem('authToken'))

const router = useRouter();
const route = useRoute();
const store = useCounterStore();

const personId = route.params.person_id;
const user = ref({});
const activeTab = ref('articles'); // 기본 탭 설정

// 자신의 프로필 여부 확인
const isOwnProfile = computed(() => store.loggedInUser?.pk === parseInt(personId));

onMounted(() => {
  if (isOwnProfile.value) {
    user.value = store.loggedInUser; // 자신의 프로필 데이터 사용
  } else {
    axios.get(`http://127.0.0.1:8000/accounts/profile/${personId}/`).then((res) => {
      user.value = res.data;
    });
  }
});

// 찜 콘텐트
onMounted(() => {
  document.body.style.background = '#572200'
  if (token.value) {
    cart.getCart(); // 토큰이 있을 때만 호출
  } else {
    console.log("토큰이 없습니다. 로그인하세요.");
  }
})

const editProfile = () => {
  router.push({ name: 'EditProfile', params: { person_id: personId } });
};

const goToCreateArticle = () => {
  router.push({ name: 'CreateArticleView' });
};

const goToChange = () => {
  router.push({ name: 'ChangePasswordView' })
}
onBeforeUnmount(() => {
  document.body.style.background = '' // 기본 배경으로 복원
});



</script>

<style scoped>
/* 전체 컨테이너 */
.mypage-container {
  max-width: 80%;
  margin: 0 auto;
  /* padding: 20px; */
}

/* 프로필 섹션 */
.profile-section {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.profile-info {
  display: flex;
  align-items: center;
  gap: 20px;
}

.profile-picture {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  background-color: #ddd;
}

.profile-details h2 {
  font-size: 1.5rem;
  font-weight: bold;
}

.profile-details p {
  font-size: 0.9rem;
  color: #fff;
}

.profile-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}


button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  background-color: transparent;
  color: #FFE474; 
  cursor: pointer;
  transition: all 0.3s ease; /* 부드러운 전환 효과 */
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 버튼 호버 효과 */
button:hover {
  background-color: #FFE474; /* 호버 시 배경색 변경 */
  color: #572200; /* 호버 시 텍스트 색상 변경 */
}

/* 탭 섹션 */
.tabs-section {
  display: flex;
  justify-content: center;
  border-bottom: 1px solid #ddd;
  margin-bottom: 20px;
}

.tabs-section button {
  flex: 1;
  padding: 10px 0;
  font-size: 1rem;
  background: none;
  border: none;
  cursor: pointer;
  color: #fff;
  font-weight: bold;
}

.tabs-section button.active {
  border-bottom: 2px solid #fff;
  color: #FFE474;
}

/* 콘텐츠 섹션 */
.content-section {
  margin-top: 20px;
}

.cart-item-list {
  display: flex;
  flex-wrap: wrap; /* 자식 요소들이 가로로 정렬되며 공간이 부족하면 줄바꿈 */
  gap: 20px; /* 아이템 간의 간격 */
  justify-content: flex-start; /* 왼쪽 정렬 */
  align-items: flex-start;
}

</style>
