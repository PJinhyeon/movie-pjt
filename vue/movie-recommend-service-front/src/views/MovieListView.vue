<template>
  <div>
    <h1>MovieListView</h1>
    <div>
        <GenreFilter  @genreSelected="onGenreSelected"/>
        <!-- <GenreFilter @genreSelected="onGenreSelected"/> -->
        <!-- <GenreFilter @genreSelected="filterByGenre" /> -->
         <SortToggle/>
        <!-- <SortToggle @sortChanged="sortMovies" /> -->
      </div>
    <MovieList/>
    <!-- {{ genreresult }} -->
    <!-- <MovieList :movies="sortedMovies" /> -->
  </div>
</template>

<script setup>
import GenreFilter from '@/components/GenreFilter.vue';
import SortToggle from '@/components/SortToggle.vue';
import MovieList from '@/components/MovieList.vue';

import { useCounterStore } from '@/stores/counter';
import { onMounted, ref } from 'vue';

const store = useCounterStore()
onMounted(() => {
  store.fetchGenres()
})

const selectedGenre = ref('')

const onGenreSelected = (genreId) => {
  selectedGenre.value = genreId; // "all" 또는 특정 장르 ID를 저장
  console.log(selectedGenre.value)
};




</script>

<style scoped>

</style>