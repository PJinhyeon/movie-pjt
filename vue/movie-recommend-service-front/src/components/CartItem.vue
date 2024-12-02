<template>
  <div class="cart-item-container">
    <div 
      v-if="movie" 
      class="cart-item" 
      @click="onClick(movie)"
    >
      <MovieCard :movie="movie" />
    </div>
    <div v-else class="loading-message">
      로딩 중...
    </div>
  </div>
</template>

<script setup>
import { ref, watchEffect } from 'vue';
import axios from 'axios';
import MovieCard from '@/components/MovieCard.vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  cartItem: Object,
});

const movie = ref(null);
const router = useRouter();

watchEffect(() => {
  if (props.cartItem?.id) {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/movies/${props.cartItem.movie}/`,
    })
      .then((res) => {
        movie.value = res.data;
      })
      .catch((err) => {
        console.error('영화 정보를 가져오는 중 에러 발생:', err);
      });
  }
});

const onClick = function (movie) {
  router.push({
    name: 'MovieDetailView',
    params: { movie_id: movie.id },
  });
};
</script>

<style scoped>
</style>
