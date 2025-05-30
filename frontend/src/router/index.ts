import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import MostPlayedView from '../views/MostPlayedView.vue'
import UserPlaytimeView from '../views/UserPlaytimeView.vue'
import PopularPlaylistsView from '../views/PopularPlaylistsView.vue'
import UserPlaylistsView from '../views/UserPlaylistsView.vue'
import PlaylistDetailsView from '../views/PlaylistDetailsView.vue'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView
    },
    {
      path: '/my-playlists',
      name: 'my-playlists',
      component: UserPlaylistsView,
      meta: { requiresAuth: true }
    },
    {
      path: '/playlist/:id',
      name: 'playlist-details',
      component: PlaylistDetailsView,
      props: true
    },
    {
      path: '/most-played',
      name: 'most-played',
      component: MostPlayedView
    },
    {
      path: '/user-playtime',
      name: 'user-playtime',
      component: UserPlaytimeView
    },
    {
      path: '/popular-playlists',
      name: 'popular-playlists',
      component: PopularPlaylistsView
    }
  ]
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.loggedIn) {
    next({ name: 'login' })  // or show a not-authorized page
  } else {
    next()
  }
})

export default router
