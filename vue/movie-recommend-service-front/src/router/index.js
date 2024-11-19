import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LoginView from '@/views/LoginView.vue'
import MovieListView from '@/views/MovieListView.vue'
import MovieDetailView from '@/views/MovieDetailView.vue'
import GenreView from '@/views/GenreView.vue'
import testView from '@/views/testView.vue'
import MyPageView from '@/views/MyPageView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomeView',
      component: HomeView,
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView
    },
    {
      path: '/login',
      name: 'LoginView',
      component: LoginView
    },
    {
      path: '/movies',
      name: 'MovieListView',
      component: MovieListView,
    },
    {
      path: '/movies/:movie_id',
      name: 'MovieDetailView',
      component: MovieDetailView,
      props: true,
    },
    {
      path: '/movies/genre/:genre_id', 
      name: 'GenreView', 
      component: GenreView 
    },
    // movie card, movie detail 테스트 위해 임시로 만든 페이지. MovieList 구성에 이용 예정
    {
      path: '/test', 
      name: 'testView', 
      component: testView 
    },
    {
      path: '/profile/:person_id', 
      name: 'MyPageView', 
      component: MyPageView
    }
  ],
})

export default router
