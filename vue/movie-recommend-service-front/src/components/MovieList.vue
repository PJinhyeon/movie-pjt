<template>
  <div class="movie-list">
    <MovieCard 
      v-for="movie in movies" 
      :key="movie.id" 
      :movie="movie" 
      @click.prevent="onClick(movie)" 
    />
  </div>
</template>

<script setup>
import MovieCard from '@/components/MovieCard.vue'
import router from '@/router'

const props = defineProps({
  movies: Array
})

const onClick = (movie) => {
  router.push({
    name: 'MovieDetailView',
    params: { movie_id: movie.id },
  })
}
</script>

<style scoped>
.movie-list {
  display: flex;
  flex-wrap: wrap; /* 아이템들이 가로로 정렬되며 공간이 부족하면 줄바꿈 */
  gap: 20px; /* 카드 간 간격 */
  justify-content: flex-start; /* 왼쪽 정렬 */
}
</style>
