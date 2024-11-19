<template>
  <div>
    <h1>MovieListView</h1>
    <div>
      <GenreFilter @genreSelected="onGenreSelected"/>
    </div>

    <!-- MovieList.vue에 props -->
    <!-- <MovieList :movies="filteredMovies" /> 
    {{ filteredMovies }} -->


    <!-- <MovieList v-if="store.movies" :movies="filteredMovies" /> -->
    <div v-if="store.movies">{{ filteredMovies }}</div>
    <div v-else>Loading movies...</div>


  </div>
</template>


<script setup>
import GenreFilter from '@/components/GenreFilter.vue';
import MovieList from '@/components/MovieList.vue';

import { useCounterStore } from '@/stores/counter';
import { onMounted, ref, computed } from 'vue';

const store = useCounterStore()
onMounted(() => {
  store.fetchGenres()
  store.getMovies()
})


// "all" 또는 특정 장르 ID를 저장
const selectedGenre = ref('all')

const onGenreSelected = (genreId) => {
  selectedGenre.value = genreId
}

const filteredMovies = computed(() => {
  console.log('디버깅:', store.movies)
  // 모든 영화
  if (selectedGenre.value === 'all') {
    return store.movies
  } 
  // 선택된 장르에 맞는 영화 필터링
  return store.movies.filter((movie) => movie.genres.includes(selectedGenre.value))
})


</script>


<style scoped>


</style>