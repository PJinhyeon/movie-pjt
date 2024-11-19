import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const router = useRouter()
  // state
  const movies = ref([])
  const genres = ref([])
  const token = ref(null) // 인증 토큰 저장
  // 현재 로그인 상태를 저장
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else{
      return true
    }
  })
  const loggedInUser = ref(null) // 로그인한 사용자 객체 전체를 저장
  // getters

  if (localStorage.getItem('authToken')) {
    token.value = localStorage.getItem('authToken');
  }

  // actions
  const signUp = function (formData) {
    axios ({
      method: 'post',
      url: 'http://127.0.0.1:8000/dj-rest-auth/registration/',
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data', // 파일 업로드를 위한 헤더
      },
    })
      .then((res) => {
        console.log('성공 : ', res)
      })
      .catch((err) => {
        console.log('에러 : ', err)
      })
  }

  const logIn = function (payload) {
    const { username, password } = payload
    axios ({
      method: 'post',
      url: 'http://127.0.0.1:8000/dj-rest-auth/login/',
      data: {
        username, password
      }
    })
    .then((res) => {
      console.log('성공 : ', res)
      token.value = res.data.key // 토큰 저장
      fetchLoggedInUserId()
      localStorage.setItem('authToken', res.data.key); // 로컬 스토리지에 저장하여 새로고침 시 유지
    })
    .catch((err) => {
      console.log('에러 : ', err)
    })
  }

  // 로그아웃
  const logOut = function () {
    token.value = null // 토큰 초기화
    loggedInUser.value = null // 로그아웃 시 사용자 정보 초기화
    localStorage.removeItem('authToken') // 로컬 스토리지에서 토큰 제거
    console.log('로그아웃 되었습니다.')
  }

  // 장르 리스트
  const fetchGenres = function() {
    axios({
      method: 'GET',
      url: 'http://127.0.0.1:8000/movies/genres/'
    })
      .then((res) => {
        console.log(res.data)
        genres.value = res.data
      })
      .catch((err)=>{
        console.log(err)
      })
  }

  // 영화 리스트
  const getMovies = function () {
    axios ({
      method: 'get',
      url: 'http://127.0.0.1:8000/movies/'
    })
      .then((res) => {
        movies.value = res.data
      })
      .catch((err) => {
        console.log("에러 : ", err)
      })
  }

  
  // 선택된 장르(genreId)에 따라 필터
  const selectOneGenre = function(genreId) {
    const genre = genres.value.filter(g => g.id === genreId)
    console.log(genre)
    return genre
  }

  // 영화 id로 영화 객체 반환하기
  const selectOneMovie = function (movieId) {
    return movies.value.find(m => m.id === movieId)
  };

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




  return { signUp, logIn, genres, getMovies, fetchGenres, selectOneGenre, movies, selectOneMovie, token, isLogin, logOut, loggedInUser, fetchLoggedInUserId }

})