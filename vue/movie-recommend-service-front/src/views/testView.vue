<template>
  <h1>테스트</h1>
  <div style="display: flex; flex-wrap: wrap;">
    
      <MovieCard v-for="movie in movies" :key="movie.id" :movie="movie" style="margin: 5px;" @click="goToMovieDetail(movie.id)"/>
  </div>
</template>

<script setup>
import MovieCard from '@/components/MovieCard.vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const goToMovieDetail = (movieId) => {
  router.push({ name: 'MovieDetailView', params: { movie_id: movieId } });
};


const movies = [
  { 
    id: 1,
    title: "Inception",
    poster: "https://example.com/poster/inception.jpg",
    overview: "A skilled thief, the absolute best in the dangerous art of extraction, stealing valuable secrets from deep within the subconscious during the dream state.",
    release_date: "2010-07-16",
    runtime: 148,
    status: "Released",
    adult: false,
    vote_average: 8.8,
    vote_count: 21000,
    original_language: "en",
    director: "Christopher Nolan",
    watch_platforms: { netflix: true, amazon: false, disney: true },
    genres: ["Action", "Sci-Fi", "Thriller"],
    actors: ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Ellen Page"],
    keywords: ["dream", "subconscious", "heist"]
  },
  {
    id: 2,
    title: "Interstellar",
    poster: "https://example.com/poster/interstellar.jpg",
    overview: "A group of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
    release_date: "2014-11-07",
    runtime: 169,
    status: "Released",
    adult: false,
    vote_average: 8.6,
    vote_count: 18000,
    original_language: "en",
    director: "Christopher Nolan",
    watch_platforms: { netflix: false, amazon: true, disney: false },
    genres: ["Adventure", "Drama", "Sci-Fi"],
    actors: ["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"],
    keywords: ["space travel", "wormhole", "future"]
  },
  {
    id: 3,
    title: "The Dark Knight",
    poster: "https://example.com/poster/dark_knight.jpg",
    overview: "When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham.",
    release_date: "2008-07-18",
    runtime: 152,
    status: "Released",
    adult: false,
    vote_average: 9.0,
    vote_count: 23000,
    original_language: "en",
    director: "Christopher Nolan",
    watch_platforms: { netflix: true, amazon: true, disney: false },
    genres: ["Action", "Crime", "Drama"],
    actors: ["Christian Bale", "Heath Ledger", "Aaron Eckhart"],
    keywords: ["joker", "vigilante", "crime"]
  }
];


</script>

<style lang="scss" scoped>

</style>