<template>
  <div class="movie-list-container">
    <GenreFilter @genreSelected="onGenreSelected" />
    <MovieList :movies="filteredMovies" />
  </div>
</template>

<script setup>
import GenreFilter from '@/components/GenreFilter.vue'
import MovieList from '@/components/MovieList.vue'
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const store = useCounterStore()
onMounted(() => {
  store.getMovies()
})

const route = useRoute()
const router = useRouter()

const selectedGenre = ref(route.params.genreId || 'all')
const filteredMovies = ref(store.popular_movies)

const fetchMoviesByGenre = (genreId) => {
  if (genreId === 'all') {
    filteredMovies.value = store.popular_movies
  } else {
    axios
      .get(`http://127.0.0.1:8000/movies/genre/${genreId}/`)
      .then((response) => {
        filteredMovies.value = response.data
      })
      .catch((err) => {
        console.error('에러:', err)
      })
  }
}

const onGenreSelected = (genreId) => {
  if (genreId === 'all') {
    router.push('/movies')
  } else {
    router.push({ name: 'GenreFilteredMovies', params: { genreId } })
  }
  selectedGenre.value = genreId
}

watch(
  () => route.params.genreId,
  (newGenreId) => {
    selectedGenre.value = newGenreId || 'all'
    fetchMoviesByGenre(selectedGenre.value)
  },
  { immediate: true }
)
</script>

<style scoped>
.movie-list-container {
  display: flex;
  flex-direction: column;
  gap: 20px; /* 장르 필터와 영화 리스트 간격 */
  padding: 20px; /* 전체 여백 */
}
</style>
