import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LoginView from '@/views/LoginView.vue'
import MovieListView from '@/views/MovieListView.vue'
import MovieDetailView from '@/views/MovieDetailView.vue'
import MyPageView from '@/views/MyPageView.vue'
import CommunityView from '@/views/CommunityView.vue'
import CreateArticleView from '@/views/CreateArticleView.vue'
import ArticleDetailView from '@/views/ArticleDetailView.vue'
import SearchView from '@/views/SearchView.vue'
import CartView from '@/views/CartView.vue'
import ArticleUpdateView from '@/views/ArticleUpdateView.vue'
import RecommendationView from '@/views/RecommendationView.vue'
import EditProfile from '@/views/EditProfile.vue'
import ChangePasswordView from '@/views/ChangePasswordView.vue'

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
      path: '/change',
      name: 'ChangePasswordView',
      component: ChangePasswordView
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
      path: '/movies/cart',
      name: 'CartView',
      component: CartView,
    },
    {
      path: '/genre/:genreId', 
      name: 'GenreFilteredMovies',
      component: MovieListView,
    },
    {
      path: '/profile/:person_id', 
      name: 'MyPageView', 
      component: MyPageView
    },
    {
      path: '/community', 
      name: 'CommunityView', 
      component: CommunityView
    },
    {
      path: '/community/articles/new', 
      name: 'CreateArticleView', 
      component: CreateArticleView
    },
    {
      path: '/articles/:articleId',
      name: 'ArticleDetailView',
      component: ArticleDetailView,
    },
    {
      path: '/movies/search/',
      name: 'SearchView',
      component: SearchView,
    },
    {
      path: '/articles/:articleId/update/',
      name: 'ArticleUpdateView',
      component: ArticleUpdateView,
    },
    {
      path: '/recommendations/',
      name: 'RecommendationView',
      component: RecommendationView,
    },
    {
      path: '/profile/:person_id/edit/', 
      name: 'EditProfile', 
      component: EditProfile
    }
  ],
})


export default router
