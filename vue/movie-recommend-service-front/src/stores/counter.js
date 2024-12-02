import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const router = useRouter()
  // state
  const popular_movies = ref([])
  const token = ref(null) // 인증 토큰 저장
  const loggedInUser = ref(null) // 로그인한 사용자 객체 전체를 저장

  // 로컬스토리지에서 토큰 가져오기
  if (localStorage.getItem('authToken')) {
    token.value = localStorage.getItem('authToken')

    // 토큰이 있으면 사용자 정보 가져오기
    axios({
      method: 'GET',
      url: 'http://127.0.0.1:8000/dj-rest-auth/user/',
      headers: {
        'Authorization': `Token ${token.value}`
      }
    })
      .then((res) => {
        loggedInUser.value = res.data
      })
      .catch((err) => {
        console.error('사용자 정보 가져오기 에러:', err)
        loggedInUser.value = null // 사용자 정보 가져오기 실패 시 초기화
      })
  }
 
  
  // getters
  // 현재 로그인 상태를 저장
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else{
      return true
    }
  })

  
  // actions
  // 영화 리스트
  const getMovies = function () { 
    axios ({
      method: 'get',
      url: 'http://127.0.0.1:8000/movies/'
    })
      .then((res) => {
        popular_movies.value = res.data
      })
      .catch((err) => {
        console.log("에러 : ", err)
      })
  }

  // 회원가입
  const signUp = function (formData) {
    return axios({ // 반드시 `return`을 추가
      method: 'post',
      url: 'http://127.0.0.1:8000/dj-rest-auth/registration/',
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data', // 파일 업로드를 위한 헤더
      },
    })
      .then((res) => {
        console.log('회원가입 성공:', res)
        return res; // 성공 시 응답 반환
      })
      .catch((err) => {
        console.error('회원가입 에러:', err)
        return Promise.reject(err) // 에러를 상위로 전달
      });
  };
  

  // 로그인
  const logIn = function (payload) {
    const { username, password } = payload
    return axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/dj-rest-auth/login/',
      data: {
        username,
        password
      }
    })
      .then((res) => {
        console.log('로그인 성공:', res)
        token.value = res.data.key // 토큰 저장
        fetchLoggedInUserId()
        localStorage.setItem('authToken', res.data.key) // 로컬 스토리지에 저장
        return res // 성공 시 응답 반환
      })
      .catch((err) => {
        console.error('로그인 에러:', err)
        return Promise.reject(err) // 에러를 상위로 전달
      })
  }

  // 비밀번호 변경
  const changePassword = function (payload) {
    return axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/dj-rest-auth/password/change/',
      headers: {
        'Authorization': `Token ${token.value}`
      },
      data: payload
    })
      .then((res) => {
        console.log('비밀번호 변경 성공: ', res.data)
      })
      .catch((err) => {
        console.error('비밀번호 변경 에러: ', err.response ? err.response.data : err)
      })
  }
  

  // 로그아웃
  const logOut = function () {
    token.value = null // 토큰 초기화
    loggedInUser.value = null // 로그아웃 시 사용자 정보 초기화
    localStorage.removeItem('authToken') // 로컬 스토리지에서 토큰 제거
    console.log('로그아웃 되었습니다.')
  }

  const fetchLoggedInUserId = function () {
    if (token.value) {
      axios({
        method: 'GET',
        url: 'http://127.0.0.1:8000/dj-rest-auth/user/',
        headers: {
          'Authorization': `Token ${token.value}`
        }
      })
        .then((res) => {
          console.log('사용자 정보 가져오기 성공:', res)
          loggedInUser.value = res.data // 로그인 성공 시 사용자 정보를 저장
        })
        .catch((err) => {
          console.log('사용자 정보 가져오기 에러:', err)
        })
    }
  }

  const moviesWithMostArticles = ref([]); // 게시글이 많은 영화 데이터 저장

  const fetchMoviesWithMostArticles = function () {
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/movies/movies-with-most-articles/', // 게시글이 많은 영화 데이터 API
    })
      .then((res) => {
        moviesWithMostArticles.value = res.data; // 데이터를 스토어에 저장
      })
      .catch((err) => {
        console.error('게시글 많은 영화 데이터 가져오기 에러:', err);
      });
  };
  
  
  return { popular_movies, getMovies, signUp, logIn, changePassword, token, isLogin, logOut, loggedInUser, fetchLoggedInUserId, fetchMoviesWithMostArticles, moviesWithMostArticles }

})

