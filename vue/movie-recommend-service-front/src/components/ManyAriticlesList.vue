<template>
  <div>
    <div v-if="moviesWithMostArticles.length > 0" class="movie-list">
      <div v-for="movie in moviesWithMostArticles" :key="movie.movie_id">
        <MovieCard :movie="movie" @click.prevent="onClick(movie)" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router';
import MovieCard from './MovieCard.vue';

const router = useRouter();
const store = useCounterStore();
const { moviesWithMostArticles } = storeToRefs(store);

const onClick = (movie) => {
  router.push({
    name: 'MovieDetailView',
    params: { movie_id: movie.id },
  });
};

// 컴포넌트 마운트 시 데이터 가져오기
store.fetchMoviesWithMostArticles();
</script>

<style scoped>
.movie-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}
</style>
