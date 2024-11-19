# movie-pjt
SSAFY 1학기 관통  PJT

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
 >> 해결 : model을 만들 때는, 필드 하나만 추가하면 n:m의 관계를 자동을 만들어 줌.
          하지만, ERD에서는 다 만들어 줘야 함. 표현할 수 없기 때문 => ex) MovieActor

## 11.19
회원가입 폼을 커스텀 하는 부분에서 어려움이 있었음. 
알고보니 pjt-10에 pdf자료로 있었음...
구글링이랑 지피티로 엄청 했을때 안되었던 것이 갑자기 잘만됨 ;;ㅋ큐ㅠ
pdf 설명에서 공식 자료와 공식 git을 보라고 해 주셨음. 꿀팁이다~b

vue에서 컴포넌트 구조를 생각하는 부분이 어려웠음. 계속 햇던 것인데.. 구조도 똑같은데.. 막상 처음부터 하려니 어려웠다. 
그동안 너무 아무생각없이 따라만 했다는것을 또 한번 느꼈고, 이렇게 또 한번 배웠다.
