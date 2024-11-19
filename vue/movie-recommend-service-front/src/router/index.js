import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LoginView from '@/views/LoginView.vue'
import MovieListView from '@/views/MovieListView.vue'
import MovieDetailView from '@/views/MovieDetailView.vue'
import GenreView from '@/views/GenreView.vue'

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
      path: '/movies/:movie_pk',
      name: 'MovieDetailView',
      component: MovieDetailView,
    },
    {
      path: '/movies/genre/:genre_pk', 
      name: 'GenreView', 
      component: GenreView 
    }
  ],
})

export default router
