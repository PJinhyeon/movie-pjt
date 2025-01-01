# **영화 추천 시스템**
## **1. 팀원 정보 및 업무 분담 내역**

| 이름  | 담당 업무 |
|-------|-----------|
| 공통 | 프로젝트 기획, ERD 작성, 목업, 더미 데이터 생성, Movie App, Recommendation App |
| 박진현  | Community App, Search App, HomeView.vue |
| 임지혜  | Account App, 영화 찜 기능&장르 필터(Movie App), 검색 기록 관리(Search App), MyPageView.vue |

**[참고] 구체적인 업무 내역**  

---

## **2. 목표 서비스 구현 및 실제 구현 정도**
### **목업**
[figma](https://www.figma.com/design/AaaTIDVl7GqueiJOSmuh0h/JHs'-%EA%B4%80%ED%86%B5?node-id=0-1&node-type=canvas&t=xPa0EAh3DoDJZOnl-0)

### **목표 ERD**
[ERD](https://dbdiagram.io/d/%EC%98%81%ED%99%94-%EC%B6%94%EC%B2%9C-%EC%B4%88%EC%95%88-6745ed82e9daa85acac7ffc3)



### **실제 구현 ERD**
[ERD](https://dbdiagram.io/d/%EC%98%81%ED%99%94-%EC%B6%94%EC%B2%9C-673ad1b3e9daa85acac7573a)

---

## **3. 영화 추천 알고리즘에 대한 기술적 설명, 생성형 AI 활용한 부분**

Recommendation App의 영화 추천 알고리즘은 **업로드된 이미지를 분석**하고, 이를 기반으로 **사용자에게 적합한 영화를 추천**합니다. **Google Vision API**, **GPT API**, **TMDB API**, 그리고 **sentence-transformers** 라이브러리를 조합하여 강력한 추천 시스템을 구현했습니다.

### **주요 알고리즘 구성 요소**
- **Google Vision API**  
  사용자가 업로드한 이미지를 분석하여 이미지에서 추출된 시각적 정보를 **키워드 형태**로 반환합니다.
- **GPT API**  
  Vision API에서 추출된 키워드를 기반으로 **TMDB 키워드**와 매칭합니다. GPT API는 **문맥적 이해**를 바탕으로 키워드 간의 연관성을 매칭하도록 설계되었습니다.
- **TMDB API**  
  매칭된 **TMDB 키워드**를 바탕으로 **TMDB 데이터베이스**에서 관련된 영화 데이터를 검색합니다.
- **Sentence-Transformers**  
  GPT API만으로 키워드 매칭에서 발생하던 문제를 해결하기 위해 추가로 도입된 기술입니다. 텍스트 임베딩을 통해 키워드 간의 **문맥적 유사성**을 계산하고, GPT API의 매칭 결과를 보완합니다.  
  예: "action adventure"와 "adventure action" 같은 키워드의 유사성을 인식.

### **추천 알고리즘의 주요 프로세스**
1. **이미지 업로드 및 처리**  
   사용자가 업로드한 이미지를 Google Vision API로 분석하여 키워드를 추출.
2. **TMDB 키워드 매칭**  
   GPT API와 sentence-transformers를 사용하여 Vision API 키워드를 TMDB 키워드 리스트와 매칭.  
   GPT API는 키워드 매칭 결과를 생성하며, sentence-transformers는 유사도를 기반으로 GPT의 결과를 보완.
3. **영화 데이터 검색**  
   TMDB API를 호출하여 매칭된 키워드와 관련된 영화 데이터를 검색.
4. **추천 결과 저장 및 조회**  
   추천된 영화 목록은 사용자별로 데이터베이스(RecommendedResult)에 저장되어, 사용자는 이를 조회, 삭제하거나 새로 추천받을 수 있음.

### **개발 과정에서의 위기와 극복**
- **위기 1: 이미지 분석 문제**  
  - **문제**: 처음에는 GPT API를 사용하여 업로드된 이미지를 직접 분석하고 TMDB 키워드와 매칭하려고 했습니다. 그러나 챗 GPT와의 대화에서 GPT API가 이미지를 인식할 수 없다는 사실을 알게 되어 낙담했습니다.  
  - **해결**: 대안을 모색하던 중, Google Vision API를 발견하였고, 이를 사용하여 이미지를 분석하고 시각적 정보를 키워드로 변환하는 방법을 도입했습니다.  
  - **결과**: Vision API는 이미지 분석에 강력한 성능을 제공하여 키워드 추출 과정을 성공적으로 수행할 수 있었습니다.
  
- **위기 2: TMDB 키워드 매칭 오류**  
  - **문제**: GPT API가 Vision API 키워드를 TMDB 키워드와 매칭하는 과정에서 TMDB에 없는 키워드를 반환하거나, 매칭 결과가 정확하지 않아 추천 알고리즘의 신뢰도가 떨어졌습니다.  
  - **해결**: 텍스트 임베딩과 유사도 계산에 강력한 sentence-transformers를 추가로 도입했습니다. Vision API와 TMDB 키워드 간의 유사도를 계산하여 GPT API의 결과를 보완하도록 설계했습니다.  
  - **결과**: 키워드 매칭의 정확도가 크게 향상되어 TMDB와의 통합성이 개선되었고, 추천 결과의 품질도 높아졌습니다.

---

## **4. 핵심 기능에 대한 설명**

### **1. 이미지 업로드 기반 영화 추천**
- 사용자가 업로드한 이미지를 Google Vision API로 분석하여 키워드를 추출.  
- GPT API와 sentence-transformers를 활용해 TMDB 키워드와 매칭.  
- TMDB API를 통해 관련 영화 데이터를 검색하고, 사용자 맞춤형 추천을 제공합니다.

### **2. 카테고리별 영화 조회 (장르, 주제별)**
- TMDB API를 사용해 액션, 드라마, 코미디 등 다양한 장르 및 주제별 영화 목록을 탐색 가능.  
- 인기 영화와 사용자 관심사에 맞는 영화를 쉽게 찾을 수 있습니다.

### **3. 커뮤니티 기능**
- 사용자들이 영화에 대한 리뷰, 질문, 토론 주제를 게시하고 상호작용할 수 있는 공간 제공.  
- 댓글 기능을 통해 사용자 간 의견을 공유하고, 인기 게시글을 확인할 수 있습니다.


---
### <지혜와 진현이의 눈물의 개발 일기>
## 11.18
1. 페이지 UI 완성
2. ERD
3. 장고, 뷰 프로젝트 및 requirements 파일 생성
4. 어플리케이션 전체 테마 결정
 
어려웠던 점...
- ERD 어떤 사이트를 사용해야 하는지 고민이 되었음 : https://dbdiagram.io/home
- ERD 만드는데 모델과 필드를 어떻게 만들어야 하는지 고민되었음
 예를 들어, 영화 모델, 장르모델, 영화-장르 연결 모델을 다 따로 만들어야 하는지
 아니면 그냥 영화 모델, 장르모델 두 개만 만들고
 영화 모델의 필드 중 하나로 장르 필드 만들어서 저장해도 충분한지
- 해결 : model을 만들 때는, 필드 하나만 추가하면 n:m의 관계를 자동을 만들어 줌.
          하지만, ERD에서는 다 만들어 줘야 함. 표현할 수 없기 때문 => ex) MovieActor

## 11.19
회원가입 폼을 커스텀 하는 부분에서 어려움이 있었음. 
알고보니 pjt-10에 pdf자료로 있었음...
구글링이랑 지피티로 엄청 했을때 안되었던 것이 갑자기 잘만됨 ;;ㅋ큐ㅠ
pdf 설명에서 공식 자료와 공식 git을 보라고 해 주셨음. 꿀팁이다~b

vue에서 컴포넌트 구조를 생각하는 부분이 어려웠음. 계속 햇던 것인데.. 구조도 똑같은데.. 막상 처음부터 하려니 어려웠다. 
그동안 너무 아무생각없이 따라만 했다는것을 또 한번 느꼈고, 이렇게 또 한번 배웠다.


## 11.20

영화 장르별로 영화를 분류 하는 것이 안됨.
어렵게 장르별로 분류해 놨더니, 이제는 화면에 출력이 안됨. 대환장
하지만 해결했다! 하루종일 걸렸지만, 오늘 안에 해결해서 다행인건가..?ㅋ
해결방법 : async와 await의 역할

async는 함수를 비동기 함수로 만들고 항상 Promise를 반환하게 합니다.
await는 Promise가 완료될 때까지 기다려, 비동기 작업을 동기적으로 처리하는 것처럼 코드를 간단하게 만듭니다.
반드시 await는 async 함수 안에서만 사용 가능합니다.
필요성

기존 Promise나 콜백 체인의 복잡함을 줄이고, 가독성을 높이는 코드 작성을 돕습니다.
장르 버튼 문제 해결 요약

문제 1: filteredMovies의 비동기 로직 처리
computed가 아닌 ref로 상태를 관리하며, 비동기 요청은 별도의 함수로 처리.
문제 2: 비동기 데이터를 상태에 반영하지 않음
axios 응답 데이터를 filteredMovies에 저장하는 로직 추가.
문제 3: 라우터 변경 시 반응하지 않음
watch를 이용해 라우터 params를 감지하고 상태를 업데이트.
수정 후 코드 흐름

selectedGenre가 라우터 params에서 설정됨.
fetchMoviesByGenre 함수가 axios 요청으로 장르별 데이터를 가져옴.
watch가 라우터 params 변경을 감지해 데이터를 갱신.
버튼 클릭 시 라우터를 통해 경로 변경 및 상태 갱신.

## 11.21

- 비동기 처리

반응형으로 변수를 선언하면서, 이 변수보다 화면이 먼저 로드되기도 하고 이 변수를 참조해야 하는 변수가 먼저 할당되는 등의 문제가 생겼다. 비동기 처리를 하면서, 타이밍의 문제가 생긴 것인데, 기본적으로 axios를 사용해야 한다.
axios는 비동기 처리를 도와주면서, 특정 처리 이후 어떤 과정을 실행할 수 있도록 .then의 부분과, .then이 오류일 경우 이어지는 .catch로 이루어진다. 이는 비동기 처리를 하는 async await와 try except 둘의 역할을 한 번에 하는 것이다. 그러나, 이런 경우에도 순서에서 문제가 생길 경우 화면로드의 문제라면 onMounted, 변수와 함수들 사이의 관계라면 watch, computed, watcheffect를 사용할 수 있다.
watch는 old value와 new value를 가질 수 있으며, 감시하는 변수를 지정해야 한다.
computed의 경우 일정한 값을 return 하며, 참조하는 값이 변화했을 때만 업데이트한다.
watcheffect의 경우 watch와 유사한 역할을 하지만, 감시하는 변수를 지정할 필요없이, 자동으로 참조하는 변수들을 감시한다.


## 11.22
사용자가 업로드한 이미지를 분석하여 관련 키워드를 추출하고, 이미지에서 추출된 키워드를 기반으로 TMDB 키워드와 매칭하여 영화를 추천하는 서비스
주요 기술로 Django(백엔드), Vue.js(프론트엔드), Google Vision API, OpenAI GPT API를 사용
1. Vision API를 통한 키워드 추출:
Google Vision API를 사용하여 업로드된 이미지에서 라벨(키워드)을 추출합니다.
2. OpenAI API를 활용한 TMDB 키워드 매칭
Python 함수를 작성하여 OpenAI의 GPT API를 호출해 TMDB 키워드와 매칭 작업을 수행.
작업 흐름:
이미지 분석에서 추출된 키워드(vision_keywords)와 TMDB 제공 키워드(tmdb_keywords)를 입력.
OpenAI ChatCompletion API를 사용해 가장 적합한 키워드를 매칭.
API 응답을 JSON 문자열로 반환한 뒤 Python 객체 배열로 변환.
3. API 응답 처리
OpenAI API의 응답을 Python의 JSON 모듈을 사용해 Python 객체 리스트로 변환.
반환 형식: [{"name": "keyword_name", "id": keyword_id}, ...]


첫번째 어려움 : TMDB 키워드만 모아 놓은 파일이 없었음 => 웹 크롤링을 하여 A~Z까지 단어들 크롤링 => 파일 용량이 너무 커서 문제 발생 => GPT 사용하여 데이터 처리, 키워드 최적화 => 두번째 어려움: 딕셔너리에 키워드 네임과 아이디가 각 키워드마다 저장되어 있었는데, 키워드 아이디가 tmbd 키워드의 실제 아이디와 다르게 저장되어 있었음 => 다시 웹 크롤링하여 제대로된 아이디를 찾아줌

어려움: 처음에는 챗 지피티로 이미지 분석해서 키워드 뽑아내는 작업도 다 하려고 했으나, 지피티에게 물어보니 이미지 인식은 하지 못한다고 말함.... 그래서 다른 방법들을 찾다가 Google Vision API로 해결. 하지만 나중에 알고보니(gpt api 공식문서를 보니) 비전 기능을 가지고 있어 이미지 인식이 가능하다고 함...ㅋㅋ 오늘의 교훈: 공식문서를 보자!!

---
[참고]
1. 백엔드 개발 (Django)
주요 작업:
사용자 모델 확장: AbstractUser 상속을 통해 nickname, profile_picture 필드 추가.
사용자 CRUD 기능 구현:
생성: 회원가입 시 사용자 정보 저장 및 추가 필드 처리.
읽기: 사용자 리스트 및 개별 사용자 프로필 조회 API 개발.
수정: 프로필 업데이트 및 유효성 검사 로직 구현.
삭제: 사용자 계정 삭제 기능 및 권한 검증.
신호(signal) 처리: 사용자 생성 시 인증 토큰 자동 생성.
관련 파일:
models.py, views.py, serializer.py, signals.py
2. 프론트엔드 개발 (Vue.js)
주요 작업:
CRUD 인터페이스 개발:
생성: 회원가입 화면 (SignUpView.vue) 및 필드 검증.
읽기: 사용자 프로필 및 리스트 UI (ProfileView, ProfileListView).
수정: 프로필 업데이트 화면 (EditProfileView.vue)에서 데이터 바인딩 및 에러 처리.
삭제: 사용자 계정 삭제 기능 UI 제공.
Django API와 연동: Axios를 활용한 CRUD 요청 처리.
상태 관리: Pinia를 통해 사용자 정보와 인증 상태 관리.
관련 파일:
SignUpView.vue, LoginView.vue, ChangePasswordView.vue


Community App
1. 백엔드 개발 (Django)
주요 작업:
모델 설계 및 구현:
Article 및 Comment 모델 정의 (게시글과 댓글 간의 관계 설정, ForeignKey).
영화 데이터와 연결하기 위한 movie_id 필드 추가.
CRUD API 개발:
게시글 CRUD:
전체 게시글 조회 및 작성 (article_list).
특정 게시글 상세 조회, 수정, 삭제 (article_detail).
댓글 CRUD:
게시글에 달린 댓글 조회 및 작성 (comment_list).
특정 댓글 상세 조회, 수정, 삭제 (comment_detail).
기능 추가:
외부 API(TMDB) 연동으로 영화 정보 가져오기.
인기 게시글 조회 및 검색 기능 (community_main, search_articles).
최신 게시글 제공 기능 (recent_articles).
관련 파일:
models.py, views.py, serializers.py, urls.py
2. 프론트엔드 개발 (Vue.js)
주요 작업:
UI 컴포넌트 개발:
게시글 카드 컴포넌트 (ArticleCard.vue).
게시글 리스트 페이지 (ManyArticlesList.vue).
게시글 상세 페이지 (ArticleDetailView.vue).
게시글 작성 및 수정 페이지 (ArticleUpdateView.vue, CreateArticleView.vue).
커뮤니티 메인 페이지 (CommunityView.vue).
최신 게시글 컴포넌트 (RecentArticle.vue).
API 연동:
Axios를 활용해 Django API와 통신:
게시글과 댓글의 CRUD 작업 처리.
영화 정보와 관련된 데이터 표시.
최신 게시글 표시를 위한 API 호출.
상태 관리:
Pinia를 통해 게시글 및 댓글 상태 관리.
검색어 및 필터링 상태 관리.
관련 파일:
ArticleCard.vue, ArticleMyPage.vue, ManyArticlesList.vue, ArticleDetailView.vue, ArticleUpdateView.vue, CommunityView.vue, RecentArticle.vue, CreateArticleView.vue

Movie App
1. 백엔드 개발 (Django)
주요 작업:
모델 설계 및 구현:
CartItem 모델 구현: 사용자의 찜한 영화 데이터를 관리 (movie 필드에 TMDB 영화 ID 저장).
API 개발:
영화 데이터 API:
TMDB API와 연동하여 영화 목록, 상세 정보, 출연진, 장르별 영화 제공 (movie_list, movie_detail, movie_credits, movies_by_genre, genre_list).
인기 영화 및 검색 결과 제공 (search_movies, movies_with_most_articles).
영화 찜 기능:
찜한 영화 목록 조회 및 추가 (cart_list).
찜한 영화 제거 (remove_from_cart).
기능 추가:
TMDB 외부 API 통합: API 호출 실패 시 기본 에러 처리 로직 추가.
특정 영화와 관련된 게시글 수 조회 (movies_with_most_articles).
관련 파일:
models.py, views.py, serializers.py, urls.py
2. 프론트엔드 개발 (Vue.js)
주요 작업:
UI 컴포넌트 개발:
영화 카드 컴포넌트 (MovieCard.vue).
영화 목록 페이지 (MovieList.vue, MovieListView.vue).
인기 영화 목록 페이지 (PopularMovieList.vue).
영화 상세 페이지 (MovieDetailView.vue).
찜 목록 컴포넌트 (CartItem.vue)와 찜 목록 페이지 (CartView.vue).
장르 필터 컴포넌트 (GenreFilter.vue): 사용자에게 장르별 영화를 필터링하는 인터페이스 제공.
API 연동:
Axios를 활용하여 백엔드 API와 통신:
영화 목록, 상세 정보, 장르별 영화, 찜 목록 등의 데이터 표시.
영화 찜 추가/제거 기능 구현.
장르별 영화 필터링 및 데이터를 가져오는 요청 처리.
상태 관리:
Pinia를 활용한 찜 목록 상태 및 영화 정보 상태 관리.
검색어와 필터링 데이터 상태 관리.
관련 파일:
MovieCard.vue, MovieList.vue, PopularMovieList.vue, MovieDetailView.vue, MovieListView.vue, CartView.vue, CartItem.vue, GenreFilter.vue

Search App
1. 백엔드 개발 (Django)
주요 작업:
모델 설계 및 구현:
SearchHistory 모델 구현:
사용자별 검색 기록 저장 (키워드, 영화 ID, 검색 시간).
API 개발:
검색 기록 관리:
사용자 검색 기록 조회 및 저장 (search_history_list).
검색 기록 전체 삭제 (delete_all_search_histories).
인기 검색어 기능:
검색된 영화 중 상위 검색된 영화 목록 제공 (most_searched_movies).
TMDB API 연동:
인기 검색된 영화의 상세 데이터를 TMDB에서 가져옴.
관련 파일:
models.py, views.py, serializers.py, urls.py
2. 프론트엔드 개발 (Vue.js)
주요 작업:
UI 컴포넌트 개발:
인기 검색 영화 목록 컴포넌트 (MostSearchedMovies.vue):
상위 검색된 영화 목록을 시각적으로 표시.
검색 페이지 컴포넌트 (SearchView.vue):
검색 기능 및 검색 기록 표시/삭제 UI 구현.
API 연동:
Axios를 활용해 Django API와 통신:
사용자 검색 기록 조회 및 삭제.
인기 검색 영화 데이터를 가져오는 요청 처리.
상태 관리:
Pinia 또는 컴포넌트 상태를 통해 검색 기록 및 인기 영화 데이터 관리.
관련 파일:
MostSearchedMovies.vue, SearchView.vue

Recommendation App: 역할 분담
1. 백엔드 개발 (Django)
주요 작업:
모델 설계 및 구현:
UploadedImage: 사용자 업로드 이미지를 저장.
RecommendedResult: 사용자별 추천 영화 ID와 추천 날짜 저장.
API 개발:
이미지 처리 및 추천 기능:
Google Vision API를 통해 업로드된 이미지에서 키워드 추출 (ImageUploadView).
GPT API를 활용해 TMDB 키워드와 Vision API 키워드 매칭 (MatchTMDBKeywordsView).
TMDB 키워드 기반으로 추천 영화 목록 생성 (movies_by_keywords).
추천 관리:
추천 결과 저장 (save_recommendation).
사용자별 추천 결과 조회 (user_recommendations).
특정 추천 상세 조회 및 삭제 (recommendation_detail, delete_recommendation).
관리자 전용 추천 결과 조회 (all_recommendations).
외부 API 통합:
Google Vision API 및 GPT API 연동.
TMDB API를 활용해 키워드 기반 영화 데이터 수집.
관련 파일:
models.py, views.py, serializers.py, urls.py, gpt_utils.py, tmdb_keywords.json
2. 프론트엔드 개발 (Vue.js)
주요 작업:
UI 컴포넌트 개발:
이미지 업로드 및 결과 표시:
이미지 업로드 컴포넌트 (ImageUpload.vue).
추천된 이미지 결과 표시 컴포넌트 (ImageResult.vue).
추천 영화:
추천 영화 목록 컴포넌트 (RecommendedMovies.vue).
API 연동:
Axios를 활용하여 Django 백엔드와 통신:
이미지 업로드 및 Vision API 키워드 추출 요청.
TMDB 키워드 매칭 요청 및 추천 결과 가져오기.
추천 저장, 조회, 삭제 요청 처리.
상태 관리:
Pinia를 사용하여 사용자 추천 결과 및 키워드 매칭 데이터를 관리.
관련 파일:
ImageUpload.vue, ImageResult.vue, RecommendedMovies.vue

 추가 작업
HomeView.vue
메인 홈 화면에 사용자 맞춤형 추천 영화, 인기 영화, 및 기타 카테고리별 영화 섹션을 배치.
직관적인 네비게이션을 통해 다른 페이지로 쉽게 이동할 수 있는 인터페이스 구현.
MyPageView.vue
사용자 개인 정보를 표시하는 UI 구성 (e.g., 프로필 사진, 이름, 이메일).
사용자가 추천받은 영화와 찜한 영화 목록을 확인하고 관리할 수 있는 인터페이스 제공.



---
## Git 사용법

1. git clone main
   
2. branch 생성 : git branch tmdb
                 git branch youtube
3. branch로 변경 : git switch youtube
                  git branch youtube

(각자 작업 후 ...)

4. 첫번째 branch는 평소대로 push 가능(충돌x) : git add -> git commit -> git push tmdb
5. 두번째 branch push (충돌 발생) : git add -> git commit -> ...
  git switch main
  git pull origin main
  git merge youtube
  git add . (메인 저장) -> git commit -> git push


### git branch로 변경하는 법
1. git fetch origin
2. git branch -r
3. git checkout 브랜치명
