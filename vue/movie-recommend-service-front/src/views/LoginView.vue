<template>
  <div class="login-container">
    <h1>로그인</h1>
    <form @submit.prevent="logIn" class="login-form">
      <label for="username">아이디</label>
      <input type="text" id="username" v-model="username" placeholder="아이디를 입력하세요">

      <label for="password">비밀번호</label>
      <input type="password" id="password" v-model="password" placeholder="비밀번호를 입력하세요">

      <input type="submit" value="로그인하기" class="submit-btn">
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useCounterStore } from '@/stores/counter';
import { useRouter } from 'vue-router';

const router = useRouter()
const username = ref(null)
const password = ref(null)

const store = useCounterStore()

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value
  }

  store.logIn(payload)
    .then(() => {
      // 로그인 성공 시 HomeView로 이동
      router.push({ name: 'HomeView' })
    })
    .catch((err) => {
      // 로그인 실패 시 에러 메시지 출력
      alert('로그인에 실패했습니다. 다시 시도해주세요.')
      console.error('로그인 에러:', err)
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
.login-container {
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
.login-container h1 {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  color: #874D17; /* 진한 갈색 */
}

/* 폼 스타일 */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.login-form label {
  font-size: 1rem;
  text-align: left;
  margin-bottom: 0.5rem;
}

/* 입력 필드 스타일 */
.login-form input[type="text"],
.login-form input[type="password"] {
  border: 1px solid #BF883C; /* 황토색 테두리 */
  border-radius: 5px;
  padding: 0.8rem;
  font-size: 1rem;
  color: #874D17; /* 진한 갈색 */
  background-color: #f7f4ef; /* 연한 아이보리 */
  outline: none;
}

.login-form input[type="text"]::placeholder,
.login-form input[type="password"]::placeholder {
  color: #BF883C; /* 황토색 */
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
