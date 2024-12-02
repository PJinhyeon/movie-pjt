<template>
  <div class="edit-profile-container">
    <!-- 헤더 -->
    <header class="edit-header">
      <h1>프로필 수정</h1>
    </header>

    <!-- 프로필 수정 폼 -->
    <form v-if="!loading" @submit.prevent="updateProfile" class="edit-profile-form">
      <!-- 사용자 이름 -->
      <div class="form-group">
        <label for="username" class="form-label">사용자 이름</label>
        <input type="text" id="username" v-model="profile.username" class="form-input" />
      </div>

      <!-- 이메일 -->
      <div class="form-group">
        <label for="email" class="form-label">이메일</label>
        <input type="email" id="email" v-model="profile.email" class="form-input" />
      </div>

      <!-- 프로필 사진 -->
      <div class="form-group">
        <label for="profile_picture" class="form-label">프로필 사진</label>
        <div class="profile-picture-container">
          <img :src="profile.profile_picture || defaultProfileImage" alt="Profile Picture" class="profile-picture" />
          <input type="file" id="profile_picture" @change="onFileChange" class="file-input" />
        </div>
      </div>

      <!-- 수정 버튼 -->
      <div class="button-group">
        <button type="submit" class="save-button">저장</button>
      </div>
    </form>

    <!-- 로딩 중 메시지 -->
    <p v-else class="loading-text">데이터를 불러오는 중입니다...</p>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useCounterStore } from "@/stores/counter"; // Pinia 스토어 가져오기
import defaultProfileImage from "@/assets/default-profile.png";
import axios from "axios";
import { useRouter } from "vue-router";
const router = useRouter()

const store = useCounterStore(); // Pinia 스토어 사용
const profile = ref({
  id: null,
  username: "",
  email: "",
  profile_picture: null,
});
const newProfilePicture = ref(null); // 새로 업로드된 파일
const loading = ref(true); // 로딩 상태

// 사용자 정보 감시
watch(
  () => store.loggedInUser,
  (newUser) => {
    if (newUser) {
      profile.value = { ...newUser }; // 사용자 정보를 프로필에 로드
      loading.value = false;
    }
  },
  { immediate: true }
);

// 파일 선택 처리
const onFileChange = (event) => {
  newProfilePicture.value = event.target.files[0];
};

// 프로필 수정 요청
const updateProfile = () => {
  const formData = new FormData();
  formData.append("username", profile.value.username);
  formData.append("email", profile.value.email);
  if (newProfilePicture.value) {
    formData.append("profile_picture", newProfilePicture.value);
  }

  const token = store.token; // Pinia 스토어에서 인증 토큰 가져오기

  axios
    .put("http://127.0.0.1:8000/accounts/profile/1/", formData, {
      headers: {
        Authorization: `Token ${token}`, // 인증 헤더 추가
        "Content-Type": "multipart/form-data",
      },
    })
    .then(() => {
      alert("프로필이 성공적으로 수정되었습니다!");
      store.fetchLoggedInUserId(); // 스토어에서 사용자 정보 갱신
      router.push({ name: "MyPageView", params: { person_id: profile.id } });
    })
    .catch(() => {
      alert("프로필 수정 중 오류가 발생했습니다.");
    });
};

// 사용자 정보가 없으면 스토어를 통해 정보 가져오기
onMounted(() => {
  if (!store.loggedInUser) {
    store.fetchLoggedInUserId();
  }
});
</script>

<style scoped>
/* 전체 컨테이너 */
.edit-profile-container {
  max-width: 600px; /* 너비 조정 */
  margin: 40px auto; /* 세로 및 가로 중앙 정렬 */
  padding: 24px;
  background-color: #f7f4ef; /* 연한 아이보리 */
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* 외곽 그림자 */
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 헤더 */
.edit-header {
  text-align: center;
  margin-bottom: 30px;
}

.edit-header h1 {
  font-size: 2rem;
  color: #874d17; /* 진한 갈색 */
}

/* 폼 그룹 */
.form-group {
  margin-bottom: 24px;
  width: 100%;
  max-width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center; /* 중앙 정렬 */
}

.form-label {
  display: block;
  font-size: 1rem;
  color: #572200; /* 어두운 갈색 */
  margin-bottom: 8px;
  text-align: center; /* 중앙 정렬 */
}

.form-input,
.file-input {
  width: 80%; /* 입력 필드 너비 조정 */
  padding: 12px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #ffffff;
}

.file-input {
  border: none;
}

/* 프로필 사진 섹션 */
.profile-picture-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.profile-picture {
  width: 120px; /* 프로필 사진 크기 조정 */
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 사진 그림자 추가 */
}

/* 버튼 그룹 */
.button-group {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.save-button {
  padding: 12px 24px;
  background-color: #874d17; /* 진한 갈색 */
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.2rem;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.save-button:hover {
  background-color: #572200; /* 어두운 갈색 */
  transform: scale(1.05); /* 버튼 확대 효과 */
}

/* 로딩 텍스트 */
.loading-text {
  text-align: center;
  font-size: 1.2rem;
  color: #874d17; /* 진한 갈색 */
}
</style>

