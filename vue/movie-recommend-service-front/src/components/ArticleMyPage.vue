<template>
  <div class="article-grid">
    <div v-if="articles.length" class="grid">
      <RecentArticle v-for="article in articles" :key="article.id" :article="article" />
    </div>
    <div v-else>
      <p>작성한 게시글이 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import RecentArticle from './RecentArticle.vue';

const route = useRoute();
const articles = ref([]);

onMounted(() => {
  const personId = route.params.person_id;
  axios.get(`http://127.0.0.1:8000/community/user/${personId}/articles/`).then((res) => {
    articles.value = res.data;
  });
});
</script>

<style scoped>
.article-grid {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
  width: 100%;
}
</style>
