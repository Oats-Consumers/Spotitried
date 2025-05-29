<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-btn icon @click="drawer = !drawer" class="ml-2 mr-2">
        <v-avatar size="48">
          <v-img :src="SpotitriedLogo" alt="Spotitried Logo" cover></v-img>
        </v-avatar>
      </v-btn>
      <v-spacer></v-spacer>
      
      <!-- Auth buttons -->
      <template v-if="!auth.loggedIn">
        <v-btn variant="text" to="/login" router>Login</v-btn>
        <v-btn variant="text" to="/register" router>Register</v-btn>
      </template>
      <template v-else>
        <v-btn variant="text" @click="auth.logout">Logout</v-btn>
      </template>
      <!-- Dark mode toggle -->
      <v-btn icon @click="isDark = !isDark">
        <v-icon>{{ isDark ? 'mdi-weather-sunny' : 'mdi-weather-night' }}</v-icon>
      </v-btn>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" app permanent>
      <v-list-item :to="{ name: 'home' }" title="Home" link />
      <v-list-item :to="{ name: 'most-played' }" title="Most Played Songs" link />
      <v-list-item :to="{ name: 'user-playtime' }" title="User Playtime" link />
      <v-list-item :to="{ name: 'popular-playlists' }" title="Popular Playlists" link />
      <v-list-item :to="{ name: 'about' }" title="About" link />
    </v-navigation-drawer>

    <v-main>
      <router-view />
    </v-main>

    <MusicPlayer></MusicPlayer>
  </v-app>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useTheme } from 'vuetify'
import SpotitriedLogo from '@/assets/cropped_spotitried_logo.png'
import MusicPlayer from './components/MusicPlayer.vue';
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

const drawer = ref(true)

const isDark = ref(true)

const theme = useTheme()

watch(isDark, (val) => {
  theme.global.name.value = val ? 'dark' : 'light'
})
</script>

<style scoped></style>
