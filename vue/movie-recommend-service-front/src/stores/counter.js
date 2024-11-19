import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const router = useRouter()
  // state

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

  const fetchGenres = function() {
    axios({
      method: 'GET',
      url: 'http://127.0.0.1:8000/movies/genres/'
    })
    .then((res) => {
      console.log(res.data)
      genres.value = res.data
    })
    .catch((error)=>{
      console.log(error)
    })
  }
  const selectOneGenre = function(genreId) {
    return genres.value.filter(g => g.id === genreId)
  }

  return { signUp, logIn, genres, fetchGenres, selectOneGenre }

})