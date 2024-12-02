<template>
    <div>
        <!-- 서비스 소개 섹션 -->
        <section class="intro-section">
            <h1>이미지를 업로드하고, 당신만의 추천 영화를 발견하세요!</h1>
            <p>사진 한 장으로 새로운 영화 탐험을 시작하세요. CHU:P 데이터와 연관된 맞춤 영화 추천을 제공합니다.</p>
        </section>

        <!-- 사용 방법 섹션 -->
        <section class="how-to-section">
            <h3>사용 방법</h3>
            <ul class="how-to-list">
                <li>
                    <strong>1단계:</strong> 이미지를 업로드하세요.<br />
                    보고 싶은 영화의 분위기나 느낌을 담은 사진을 올려보세요.
                </li>
                <li>
                    <strong>2단계:</strong> 이미지를 분석합니다.<br />
                    Vision API로 이미지에서 키워드를 추출합니다.
                </li>
                <li>
                    <strong>3단계:</strong> 영화를 추천받으세요.<br />
                    데이터와 매칭된 맞춤형 영화를 추천합니다.
                </li>
            </ul>
        </section>

        <!-- ImageUpload와 ImageResult 컴포넌트 -->
        <ImageUpload @update-tmdb-movies="updateTmdbMovies" />
        <ImageResult v-if="showMovies" :movies="tmdbMovies" />
    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import ImageResult from '@/components/ImageResult.vue'
import ImageUpload from '@/components/ImageUpload.vue'

const tmdbMovies = ref([]) // TMDB에서 가져온 영화 데이터를 저장
const showMovies = ref(false) // ImageResult 표시 여부

// ImageUpload로부터 전달받은 영화 데이터를 업데이트
const updateTmdbMovies = (movies) => {
    tmdbMovies.value = movies
    showMovies.value = true // TMDB Keywords가 끝난 후 영화 리스트 표시
}

onMounted(() => {
  document.body.style.background = '#FFE474'
});

onBeforeUnmount(() => {
  document.body.style.background = '' // 기본 배경으로 복원
});
</script>

<style scoped>
/* 서비스 소개 섹션 */
.intro-section h1 {
    font-size: 2rem;
    font-weight: bold;
    color: #874D17;
    margin-bottom: 10px;
    text-align: center;
    padding-top: 40px;
}

.intro-section p {
    font-size: 1.2rem;
    color: #333;
    margin-bottom: 20px;
    text-align: center;
}

/* 사용 방법 섹션 */
.how-to-section h3 {
    font-size: 1.8rem;
    color: #874D17;
    margin-bottom: 10px;
    text-align: center;
}

.how-to-list {
    list-style: none;
    padding: 0;
    text-align: left;
    max-width: 600px;
    margin: 0 auto;
}

.how-to-list li {
    margin-bottom: 15px;
    font-size: 1rem;
    line-height: 1.5;
}
</style>
