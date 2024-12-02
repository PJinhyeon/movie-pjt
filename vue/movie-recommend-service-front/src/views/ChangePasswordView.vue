<template>
  <div class="change-container">
    <h1>비밀번호 변경</h1>
    <form @submit.prevent="change" class="change-form">
      <label for="new_password1">새 비밀번호</label>
      <input type="password" id="new_password1" v-model="newPassword1">

      <label for="new_password2">새 비밀번호 확인</label>
      <input type="password" id="new_password2" v-model="newPassword2">

      <input type="submit" value="변경하기" class="submit-btn">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useCounterStore } from '@/stores/counter';
import { useRouter } from 'vue-router';

const newPassword1 = ref(null)
const newPassword2 = ref(null)

const router = useRouter()
const store = useCounterStore()

const change = function () {
  if (newPassword1.value !== newPassword2.value) {
    alert('새 비밀번호가 일치하지 않습니다.')
    return
  }
  
  const payload = {
    new_password1: newPassword1.value,
    new_password2: newPassword2.value,
  }

  store.changePassword(payload)
  router.push({ name: 'MyPageView', params: { person_id: store.loggedInUser.pk } })
}

</script>

<style scoped>
/* 컨테이너 스타일 */
.change-container {
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
.change-container h1 {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  color: #874D17; /* 진한 갈색 */
}

/* 폼 스타일 */
.change-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.change-form label {
  font-size: 1rem;
  text-align: left;
  margin-bottom: 0.5rem;
}

/* 입력 필드 스타일 */
.change-form input[type="password"] {
  border: 1px solid #BF883C; /* 황토색 테두리 */
  border-radius: 5px;
  padding: 0.8rem;
  font-size: 1rem;
  color: #874D17; /* 진한 갈색 */
  background-color: #f7f4ef; /* 연한 아이보리 */
  outline: none;
}

.change-form input[type="password"]::placeholder {
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
