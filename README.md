# movie-pjt
SSAFY 1학기 관통  PJT

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
