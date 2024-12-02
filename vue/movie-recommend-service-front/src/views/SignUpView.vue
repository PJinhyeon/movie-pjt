<template>
    <div class="signup-container">
      <h1>회원가입</h1>
      <form @submit.prevent="signUp" class="signup-form">
        <label for="username">아이디</label>
        <input type="text" id="username" v-model="username">
  
        <label for="password1">비밀번호</label>
        <input type="password" id="password1" v-model="password1">
  
        <label for="password2">비밀번호 확인</label>
        <input type="password" id="password2" v-model="password2">
  
        <label for="email">이메일</label>
        <input type="email" id="email" v-model="email">
  
        <label for="profile-picture">프로필 이미지</label>
        <input type="file" id="profile-picture" ref="fileInput" @change="handleFileChange">
  
        <input type="submit" value="가입하기" class="submit-btn">
      </form>
    </div>
  </template>
  

  <script setup>
  import { ref, onMounted, onBeforeUnmount } from 'vue';
  import { useCounterStore } from '@/stores/counter';
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  const username = ref(null);
  const password1 = ref(null);
  const password2 = ref(null);
  const email = ref(null);
  const profile_picture = ref(null);
  
  const store = useCounterStore();
  
  // 프로필 이미지 파일 선택 시 처리
  const handleFileChange = (event) => {
    profile_picture.value = event.target.files[0]
  }
  
  // 파일 입력 필드 초기화
  const fileInput = ref(null)
  
  // 회원가입 API 호출
  const signUp = function () {
    if (password1.value !== password2.value) {
      alert('비밀번호가 일치하지 않습니다.')
      return;
    }
  
    // FormData 객체 생성
    const formData = new FormData();
    formData.append('username', username.value)
    formData.append('password1', password1.value)
    formData.append('password2', password2.value)
    formData.append('email', email.value)
  
    if (profile_picture.value) {
      formData.append('profile_picture', profile_picture.value);
    }
  
    // Store의 signUp 함수 호출
    store
      .signUp(formData)
      .then(() => {
        // 성공 시 초기화
        username.value = ''
        password1.value = ''
        password2.value = ''
        email.value = ''
        if (fileInput.value) {
          fileInput.value.value = '' // 파일 입력 필드 초기화
        }
        profile_picture.value = null
  
        // 로그인 페이지로 이동
        router.push({ name: 'LoginView' })
      })
      .catch((err) => {
        // 실패 시 경고창 출력
        alert('회원가입에 실패했습니다. 다시 시도해주세요.')
        console.error('회원가입 에러 경고창:', err)
      })
  }
  onMounted(() => {
    document.body.style.background = '#572200'
  });

  onBeforeUnmount(() => {
    document.body.style.background = '' // 기본 배경으로 복원
  });
</script>

<style scoped>
/* 컨테이너 스타일 */
.signup-container {
  background-color: #f7f4ef; /* 연한 아이보리 */
  color: #874D17; /* 진한 갈색 텍스트 */
  padding: 2rem;
  border-radius: 10px;
  max-width: 400px;
  margin: 2rem auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

/* 제목 스타일 */
.signup-container h1 {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  color: #874D17; /* 진한 갈색 */
}

/* 폼 스타일 */
.signup-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.signup-form label {
  font-size: 1rem;
  text-align: left;
  margin-bottom: 0.5rem;
}

/* 입력 필드 스타일 */
.signup-form input[type="text"],
.signup-form input[type="password"],
.signup-form input[type="email"],
.signup-form input[type="file"] {
  border: 1px solid #BF883C; /* 황토색 테두리 */
  border-radius: 5px;
  padding: 0.8rem;
  font-size: 1rem;
  color: #874D17; /* 진한 갈색 */
  background-color: #f7f4ef; /* 연한 아이보리 */
  outline: none;
}

.signup-form input[type="text"]::placeholder,
.signup-form input[type="password"]::placeholder,
.signup-form input[type="email"]::placeholder {
  color: #BF883C; /* 황토색 */
}

/* 파일 입력 스타일 */
.signup-form input[type="file"] {
  padding: 0.5rem;
  font-size: 0.9rem;
  background-color: #f7f4ef; /* 연한 아이보리 */
}

/* 버튼 스타일 */
.submit-btn {
  background-color: #FFE474; /* 밝은 노란색 */
  color: #572200; /* 어두운 갈색 텍스트 */
  border: none;
  padding: 0.8rem;
  font-size: 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-btn:hover {
  background-color: #BF883C; /* 황토색 */
}
</style>
