<template>
  <div v-if="movie">
    <h1>MovieDetailView</h1>
    <h1>{{ movie.title }}</h1>
    <img :src="movie.poster" alt="Movie Poster" style="width: 300px;"/>
    <p>{{ movie.overview }}</p>
    <p>Release Date: {{ movie.release_date }}</p>
    <p>Runtime: {{ movie.runtime }} minutes</p>
    <p>Director: {{ movie.director }}</p>
    <p>Average Vote: {{ movie.vote_average }}</p>
    <p>Number of Votes: {{ movie.vote_count }}</p>
    <p>Genres: {{ movie.genres.join(', ') }}</p>
    
  </div>
</template>

<script setup>
//라우터에서 영화 id로 영화 객체 받아오기
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useCounterStore } from '@/stores/counter';

const route = useRoute();
const movieId = route.params.movie_id;
const store = useCounterStore()
const movie = ref(null)
onMounted(() => {
  movie.value = store.selectOneMovie(parseInt(movieId))
})


</script>

<style scoped>

</style>