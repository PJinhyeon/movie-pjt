<template>
  <div class="upload-container">
    <label class="custom-file-upload">
      <input type="file" @change="onFileChange" class="file-input" />
      <i class="icon-upload"></i> Choose a file...
    </label>
    
    <div v-if="previewUrl" class="preview-section">
      <img :src="previewUrl" alt="Uploaded Image" class="preview-image" />
    </div>

    <!-- Start 버튼은 이미지 업로드 시 나타남 -->
    <button v-if="previewUrl" @click="startProcess" class="upload-button">" START "</button>

    <!-- Labels 섹션 -->
    <div v-if="labelsVisible && labels.length" id="labels-section" ref="labelsSection" class="label-section">
      <ul>
        <li
          v-for="(label, index) in labels"
          :key="label"
          class="animated-label"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <span v-for="(char, charIndex) in label.split('')" :key="charIndex" class="char">
            {{ char }}
          </span>
        </li>
      </ul>
    </div>

    <!-- TMDB Keywords 섹션 -->
    <div v-if="tmdbKeywordsVisible && tmdbKeywords.length" id="tmdb-section" ref="tmdbSection" class="label-section">
      <h2>Matched TMDB Keywords:</h2>
      <ul class="keywords-container">
        <li
          v-for="(keyword, index) in tmdbKeywords"
          :key="keyword.id"
          class="typing-effect"
          :style="{ animationDelay: `${index * 0.5}s` }"
        >
          {{ keyword.name }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import axios from 'axios'

const emit = defineEmits(['update-tmdb-movies'])

const file = ref(null)
const previewUrl = ref(null)
const labels = ref([])
const tmdbKeywords = ref([])
const tmdbMovies = ref([])

// 상태 관리 변수
const labelsVisible = ref(false)
const tmdbKeywordsVisible = ref(false)

// 섹션 요소를 참조하기 위한 ref
const labelsSection = ref(null)
const tmdbSection = ref(null)

const onFileChange = (e) => {
  file.value = e.target.files[0]
  if (file.value) {
    previewUrl.value = URL.createObjectURL(file.value)
  } else {
    previewUrl.value = null
  }
}

const startProcess = async () => {
  if (!file.value) return

  const formData = new FormData()
  formData.append("image", file.value)

  try {
    // Vision API 호출
    const response = await axios.post("http://127.0.0.1:8000/recommendations/api/upload/", formData, {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    })
    labels.value = response.data.labels

    // Labels 섹션 표시
    labelsVisible.value = true
    await nextTick()

    // Labels 섹션으로 스크롤
    if (labelsSection.value) {
      labelsSection.value.scrollIntoView({ behavior: 'smooth' })
    }

    // TMDB Keywords 섹션 표시
    setTimeout(async () => {
      const processedLabels = labels.value.map(label => label.trim().toLowerCase())
      const tmdbResponse = await axios.post("http://127.0.0.1:8000/recommendations/api/match-tmdb/", {
        keywords: processedLabels
      })
      tmdbKeywords.value = tmdbResponse.data.matched_keywords

      tmdbKeywordsVisible.value = true
      await nextTick()

      // TMDB Keywords 섹션으로 스크롤
      if (tmdbSection.value) {
        tmdbSection.value.scrollIntoView({ behavior: 'smooth' })
      }

      // TMDB 영화 데이터 API 호출
      setTimeout(async () => {
        const keywordIds = tmdbKeywords.value.map((keyword) => keyword.id)

        const params = new URLSearchParams()
        keywordIds.forEach((id) => params.append("keywords", id))

        const movieResponse = await axios.get(
          `http://127.0.0.1:8000/recommendations/api/movies-by-keywords/`,
          {
            headers: {
              Accept: "application/json",
              Authorization: "Bearer YOUR_ACCESS_TOKEN"
            },
            params
          }
        )

        tmdbMovies.value = movieResponse.data
        emit("update-tmdb-movies", tmdbMovies.value)
      }, 2000)
    }, 3000) // TMDB 키워드 섹션 3초 지연
  } catch (error) {
    console.error("Error:", error)
  }
}
</script>



<style scoped>
/* 업로드 컨테이너 */
.upload-container {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
  padding: 40px;
}

/* 업로드 버튼 */
.custom-file-upload {
  display: inline-block;
  cursor: pointer;
  background-color: #FFE474;
  padding: 10px 20px;
  border-radius: 8px;
  color: #874D17;
  font-size: 16px;
  font-weight: bold;
  text-align: center;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.custom-file-upload:hover {
  background-color: #874D17;
  color: #FFE474;
}

.file-input {
  display: none;
}

.upload-button {
  display: block;
  margin: 20px auto 0;
  background-color: #FFE474;
  color: #874D17;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.upload-button:hover {
  background-color: #874D17;
  color: #FFE474;
}

/* 이미지 미리보기 */
.preview-section {
  margin-top: 20px;
}

.preview-image {
  max-width: 100%;
  height: auto;
  margin-top: 10px;
}

/* 공통 라벨 섹션 */
.label-section {
  margin-top: 20px;
  text-align: center;
}

ul {
  list-style: none;
  padding: 0;
}

.typing-effect {
  display: inline-block;
  white-space: nowrap;
  overflow: hidden;
  border-right: 2px solid #874D17; /* 타이핑 커서 효과 */
  animation: typing 2s steps(20) forwards, blink 0.5s step-end infinite alternate;
}

/* 타이핑 애니메이션 */
@keyframes typing {
  from {
    width: 0;
  }
  to {
    width: 100%;
  }
}

/* 커서 깜박임 */
@keyframes blink {
  from {
    border-color: transparent;
  }
  to {
    border-color: #874D17;
  }
}

ul {
  list-style: none;
  padding: 0;
}

li {
  margin: 8px 0;
  padding: 8px;
  color: #874D17;
  border-radius: 4px;
  font-size: 25px;
  font-weight: bold;
  line-height: 1;
  font-family: 'Poppins', sans-serif;
}

.animated-label {
  display: inline-block;
  animation: fadeInUp 0.5s ease forwards;
  transform: translateY(20px);
  opacity: 0;
}

.char {
  display: inline-block;
  animation: fadeInChar 0.5s ease forwards;
  transform: translateY(100%);
  opacity: 0;
  font-family: 'Poppins', sans-serif;
}

/* 애니메이션 */
@keyframes fadeInUp {
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes fadeInChar {
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.keywords-container {
  border: 2px solid #874D17; /* 둥근 경계선 색상 */
  border-radius: 10px; /* 경계선 둥글게 */
  padding: 20px; /* 내부 여백 추가 */
}
</style>
