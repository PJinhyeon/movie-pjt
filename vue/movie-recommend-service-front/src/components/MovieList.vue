<template>
  <div>
    <h1>MovieList</h1>
      <!-- <div>
        <GenreFilter :genres="genres" @genreSelected="filterByGenre" />
        <SortToggle @sortChanged="sortMovies" />
      </div>
    <MovieList :movies="sortedMovies" /> -->
  </div>
</template>

<script setup>
import GenreFilter from '@/components/GenreFilter.vue';
import SortToggle from '@/components/SortToggle.vue';
import MovieList from '@/components/MovieList.vue';
</script>

<style lang="scss" scoped>

</style>