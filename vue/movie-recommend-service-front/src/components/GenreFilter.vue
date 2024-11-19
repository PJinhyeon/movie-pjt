<template>
  <div>
    <h1>GenreFilter</h1>
    <button @click="selectGenre('all')">all</button>
    <button v-for="genre in store.genres" :key="genre.id" @click="selectGenre(genre.id)">
      {{ genre.name }}
    </button>
  </div>
</template>

<script setup>
import { computed, defineEmits } from 'vue';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore()

// const genres = computed(() => store.genres)
console.log(store.genres.value)

const emit = defineEmits(['genreSelected']);
const selectGenre = (genreId) => {
  emit('genreSelected', genreId);
};

</script>

<style lang="scss" scoped>

</style>