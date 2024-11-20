<template>
  <div>
    <h1>My Page</h1>
    <div v-if="user">
      <h2>{{ user.username }}님의 프로필</h2>
      <p>이메일: {{ user.email }}</p>
      <img v-if="user.profile_picture" :src="user.profile_picture" alt="Profile Picture">
      <!-- 자신의 프로필인 경우에만 보이는 내용 -->
      <div v-if="isOwnProfile">
        <button @click="editProfile">프로필 수정</button>
      </div> 
    </div>
    <div v-else>
      <p>해당 유저의 정보를 찾을 수 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useCounterStore } from '@/stores/counter';
import axios from 'axios';

const route = useRoute();
const store = useCounterStore();

const personId = route.params.person_id
const user = ref(null)

// 자신의 프로필 여부를 확인
const isOwnProfile = computed(() => store.loggedInUser?.pk === parseInt(personId))

onMounted(() => {
  if (isOwnProfile.value) {
    // 자신의 프로필일 경우 store에 있는 정보를 사용
    user.value = store.loggedInUser
  } else {
    // 다른 사용자의 프로필일 경우 서버에서 정보를 가져옴
    axios.get(`http://127.0.0.1:8000/accounts/profile/${personId}/`)
      .then((res) => {
        user.value = res.data
      })
      .catch((err) => {
        console.error('프로필 정보를 불러오는 중 에러 발생:', err)
      })
  }
})

// 프로필 수정
const editProfile = () => {
  console.log('프로필 수정 버튼 클릭')
  // 어떻게 할지 생각해야 함
}

</script>

<style scoped>

</style>