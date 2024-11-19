import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const router = useRouter()
  // state
  const movies = ref([])
  const genres = ref([]);
  
  // getters

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
    })
    .catch((err) => {
      console.log('에러 : ', err)
    })
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

  const selectOneMovie = function (movieId) {
    return movies.value.find(m => m.id === movieId)
  };


  return { signUp, logIn, genres, getMovies, fetchGenres, selectOneGenre, movies, selectOneMovie }

})