<template>
  <div class="recommendation-section" style="margin-top: 15px;">
    <!-- 배경 레이어 -->
    <div 
      class="background-layer" 
      :style="getBackgroundStyle(previousBackgroundIndex)"
    ></div>
    <!-- 새로운 사진 레이어 -->
    <div 
      class="foreground-layer" 
      :style="getForegroundStyle(currentBackgroundIndex)"
    ></div>

    <!-- 텍스트 영역 -->
    <div class="recommendation-text">
      <h1 class="highlighted-title">CHU:P</h1>
      <p class="subtitle">사진으로 영화 추천받기</p>
    </div>

    <!-- 영화 포스터 스택 -->
    <div class="image-stack">
      <div
        v-for="(poster, index) in visiblePosters"
        :key="index"
        class="stacked-image"
        :style="getPosterStyle(index)"
      >
        <img :src="poster" alt="추천 영화 포스터" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// 배경 사진과 포스터 이미지
import image1 from '@/assets/opening/picture/1.jpg';
import image2 from '@/assets/opening/picture/2.jpg';
import image3 from '@/assets/opening/picture/3.jpg';
import image4 from '@/assets/opening/picture/4.jpg';
import image5 from '@/assets/opening/picture/5.jpg';

import poster1 from '@/assets/opening/poster/1.jpg';
import poster2 from '@/assets/opening/poster/2.jpg';
import poster3 from '@/assets/opening/poster/3.jpg';
import poster4 from '@/assets/opening/poster/4.jpg';
import poster5 from '@/assets/opening/poster/5.jpg';

// 이미지 리스트
const backgroundImages = [image1, image2, image3, image4, image5];
const posterImages = [poster1, poster2, poster3, poster4, poster5];

const currentBackgroundIndex = ref(0); // 현재 전면 이미지 인덱스
const previousBackgroundIndex = ref(0); // 이전 배경 이미지 인덱스
const visiblePosters = ref([]); // 화면에 표시할 포스터 이미지
const maxStackSize = 5; // 한 번에 표시되는 포스터 수

// 이미지 순환
onMounted(() => {
  let backgroundIndex = 0;
  let posterIndex = 0;

  setInterval(() => {
    // 이전 배경 이미지 업데이트
    previousBackgroundIndex.value = currentBackgroundIndex.value;

    // 현재 배경 이미지 업데이트
    currentBackgroundIndex.value = backgroundIndex;
    backgroundIndex = (backgroundIndex + 1) % backgroundImages.length;

    // 포스터 이미지 업데이트
    if (visiblePosters.value.length >= maxStackSize) {
      visiblePosters.value.shift(); // 가장 오래된 포스터 제거
    }
    visiblePosters.value.push(posterImages[posterIndex]);
    posterIndex = (posterIndex + 1) % posterImages.length;
  }, 800); 
});

// 배경 스타일 계산
const getBackgroundStyle = (index) => ({
  backgroundImage: `url(${backgroundImages[index]})`,
  backgroundSize: 'cover',
  backgroundPosition: 'center',
  opacity: 1,
  zIndex: -2,
});

// 전경 스타일 계산
const getForegroundStyle = (index) => ({
  backgroundImage: `url(${backgroundImages[index]})`,
  backgroundSize: 'cover',
  backgroundPosition: 'center',
  animation: 'fadeIn 3s ease',
  zIndex: -1,
});

// 포스터 스타일 계산
const getPosterStyle = (index) => {
  const offset = index * 15; // 각 포스터 간격
  return {
    transform: `translateY(${offset}px)`,
    animation: `posterDrop 0.8s ease ${index * 0.2}s`, // 순차적으로 나타나는 애니메이션
    zIndex: index,
  };
};
</script>

<style scoped>
/* 추천 섹션 */
.recommendation-section {
  position: relative;
  height: 40rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  overflow: hidden;
}

/* 배경 이미지 */
.background-layer,
.foreground-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  transition: opacity 3s ease; /* 전환 효과 */
}

/* 텍스트 스타일 */
.recommendation-text {
  flex: 1;
  z-index: 1;
  color: #ffe474;
  padding: 2rem;
  margin-top: -50px; /* 텍스트를 더 위로 이동 */
}

.recommendation-text .highlighted-title {
  font-size: 12rem; /* 아주 큰 크기 */
  font-weight: 900;
  margin: 0;
  opacity: 1; /* 완전히 불투명 */
  color: #FFE474; /* 기본 밝은 노란색 */
}

.recommendation-text .subtitle {
  font-size: 2.5rem; /* 크기를 더 키움 */
  font-weight: 700;
  color: #FFE474;
  margin-top: 1rem;
}

/* 포스터 스택 */
.image-stack {
  flex: 1;
  position: relative;
  width: 400px;
  height: 500px;
  z-index: 2;
  margin-right: 25px;
}

.stacked-image {
  position: absolute;
  top: 0;
  left: 50%;
  transform-origin: center;
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.stacked-image img {
  width: 100%;
  height: auto;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
}

/* 애니메이션 */
@keyframes fadeIn {
  from {
    clip-path: inset(0 100% 0 0); /* 왼쪽에서 서서히 나타남 */
  }
  to {
    clip-path: inset(0 0 0 0);
  }
}

@keyframes posterDrop {
  from {
    transform: translateY(-200px); /* 위에서 시작 */
    opacity: 0; /* 투명하게 시작 */
  }
  to {
    transform: translateY(0); /* 원래 위치 */
    opacity: 1; /* 완전히 보이도록 */
  }
}
</style>