<template>
  <div>
    <h1>MovieList</h1>
    <MovieCard 
      v-for="movie in movies"
      :key="movie.id"
      :movie="movie"
      @click="onClick(movie)"
    />
  </div>
</template>

<script setup>
import MovieCard from '@/components/MovieCard.vue';
import router from '@/router';

defineProps({
  movies: Array
})

const onClick = function (movie) {
 router.push(`movies/${movie.id}`)
}

</script>

<style scoped>

</style>