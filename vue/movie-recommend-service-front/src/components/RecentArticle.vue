<template>
<div class="recent-card" @click="goToDetail">
    <!-- 게시글 정보 -->
    <div class="recent-content" style="padding-left: 3rem; background-color: white; height: 100%;">
        <div>
            <h3 class="recent-title">{{ article.title }}</h3>         
        </div>
        <div>
            <p class="recent-excerpt">{{ article.content }}</p>
            <div class="recent-meta">
                <span>작성자: {{ article.user }}</span>
                <span>댓글: {{ article.comments_count }}</span>
            </div>
        </div>
    </div>

    <!-- 포스터 이미지 -->
    <img
    v-if="article.movie.poster_path"
    :src="'https://image.tmdb.org/t/p/w200' + article.movie.poster_path"
    alt="Movie Poster"
    class="recent-poster"
    />
</div>
</template>
  
<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const props = defineProps({
article: {
    type: Object,
    required: true,
},
});

const goToDetail = () => {
router.push({
    name: 'ArticleDetailView',
    params: { articleId: props.article.id },
});
};
</script>

<style scoped>
.recent-card {
display: flex;
align-items: center;
/* background-color: #fff; */
border: 1px solid #ddd;
padding: 16px;
box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
cursor: pointer;
transition: transform 0.2s ease, box-shadow 0.2s ease;
height: 15rem;

}

.recent-card:hover {
transform: translateY(-5px);
box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.recent-content {
flex: 1;
margin-right: 16px;
}

.recent-title {
font-size: 1.4rem;
font-weight: bold;
color: #874d17;
margin-bottom: 8px;
}

.recent-excerpt {
font-size: 1rem;
margin-bottom: 8px;
color: #333;
}

.recent-meta {
font-size: 0.9rem;
color: #777;
display: flex;
gap: 12px;
/* margin-left: 5rem; */
}

.recent-poster {
/* width: 120px; */
height: 100%;
object-fit: cover;
}
</style>
