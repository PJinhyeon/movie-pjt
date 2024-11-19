import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios';

export const useCounterStore = defineStore('counter', () => {
  const genres = ref([]);

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

  return { genres, fetchGenres, selectOneGenre }
})
