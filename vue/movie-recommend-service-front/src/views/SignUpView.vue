<template>
    <div>
        <h1>회원가입</h1>
        <form @submit.prevent="signUp">
            <label for="username">아이디</label>
            <input type="text" id="username" v-model="username"><br>

            
            <label for="password1">비밀번호</label>
            <input type="password" id="password1" v-model="password1"><br>
            
            <label for="password2">비밀번호 확인</label>
            <input type="password" id="password2" v-model="password2"><br>
            
            <label for="email">이메일</label>
            <input type="email" id="email" v-model="email"><br>

            <label for="profile-picture">프로필 이미지</label>
            <input type="file" id="profile-picture" ref="fileInput" @change="handleFileChange"><br>

            <input type="submit" value="가입하기">
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useCounterStore } from '@/stores/counter';

const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const email = ref(null)
const profile_picture = ref(null)

const store = useCounterStore()

// 프로필 이미지 파일 선택 시 처리
const handleFileChange = (event) => {
    profile_picture.value = event.target.files[0]
}

// 폼 초기화
const fileInput = ref(null)

// 회원가입 API 호출
const signUp = function () {
    if (password1.value !== password2.value) {
        alert('비밀번호가 일치하지 않습니다.')
        return
    }

    // FormData 객체 생성
    const formData = new FormData()
    formData.append('username', username.value)
    formData.append('password1', password1.value)
    formData.append('password2', password2.value)
    formData.append('email', email.value)

    if (profile_picture.value) {
        formData.append('profile_picture', profile_picture.value)
    }

    // Store의 signUp 함수 호출
    store.signUp(formData)

    username.value = ''
    password1.value = ''
    password2.value = ''
    email.value = ''
    if (fileInput.value) {
        fileInput.value.value = ''  // 파일 입력 필드 초기화
    }
    profile_picture.value = null
}

</script>

<style scoped>

</style>