<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-btn icon @click="drawer = !drawer" class="ml-2 mr-2">
        <v-avatar size="48">
          <v-img :src="SpotitriedLogo" alt="Spotitried Logo" cover />
        </v-avatar>
      </v-btn>
      <v-spacer />
      
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

    <v-navigation-drawer
      v-model="drawer"
      :temporary="display.smAndDown._value"
      app
    >
      <v-list-item :to="{ name: 'home' }" title="Home" link />
      <template v-if="auth.loggedIn">
        <v-list-item :to="{ name: 'my-playlists' }" title="Playlists" link />
      </template>
      <v-list-item :to="{ name: 'most-played' }" title="Most Played Songs" link />
      <v-list-item :to="{ name: 'user-playtime' }" title="User Playtime" link />
      <v-list-item :to="{ name: 'popular-playlists' }" title="Popular Playlists" link />
      <v-list-item :to="{ name: 'about' }" title="About" link />
    </v-navigation-drawer>

    <v-main>
      <router-view />
    </v-main>

    <MusicPlayer />
  </v-app>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useTheme, useDisplay } from 'vuetify'
import SpotitriedLogo from '@/assets/cropped_spotitried_logo.png'
import MusicPlayer from './components/MusicPlayer.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const drawer = ref(true)
const isDark = ref(false)
const theme = useTheme()
const display = useDisplay()

onMounted(() => {
  const stored = localStorage.getItem('isDark')
  if (stored !== null) {
    isDark.value = stored === 'true'
    theme.global.name.value = isDark.value ? 'dark' : 'light'
  }

  // Auto-close drawer on small screens
  drawer.value = !display.smAndDown._value
})

watch(isDark, (val) => {
  theme.global.name.value = val ? 'dark' : 'light'
  localStorage.setItem('isDark', String(val))
})

// Adjust drawer behavior when screen size changes
watch(() => display.smAndDown._value, (isSmall) => {
  drawer.value = !isSmall
})
</script>

<style scoped></style>
