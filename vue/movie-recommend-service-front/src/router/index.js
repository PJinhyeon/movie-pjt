import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
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
