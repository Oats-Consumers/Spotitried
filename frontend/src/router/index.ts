import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import MostPlayedView from '../views/MostPlayedView.vue'
import UserPlaytimeView from '../views/UserPlaytimeView.vue'
import PopularPlaylistsView from '../views/PopularPlaylistsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView
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

export default router
