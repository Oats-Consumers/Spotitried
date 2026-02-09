<template>
  <v-app>
    <v-app-bar app color="surface" elevation="1" class="app-bar">
      <v-btn icon @click="drawer = !drawer" class="ml-2 mr-2">
        <v-avatar size="44">
          <v-img :src="SpotitriedLogo" alt="Spotitried Logo" cover />
        </v-avatar>
      </v-btn>
      <v-app-bar-title class="brand-title">Spotitried</v-app-bar-title>
      <v-spacer />

      <div class="auth-actions">
        <template v-if="!auth.loggedIn">
          <v-btn variant="text" to="/login" router>Login</v-btn>
          <v-btn variant="text" to="/register" router>Register</v-btn>
        </template>
        <template v-else>
          <v-btn variant="tonal" color="primary" @click="auth.logout">Logout</v-btn>
        </template>
      </div>

      <v-btn icon @click="isDark = !isDark" class="ml-1">
        <v-icon>{{ isDark ? 'mdi-weather-sunny' : 'mdi-weather-night' }}</v-icon>
      </v-btn>
    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      :temporary="display.smAndDown.value"
      app
      class="nav-drawer"
    >
      <v-list nav density="comfortable">
        <v-list-item :to="{ name: 'home' }" title="Home" prepend-icon="mdi-home-variant" link />
        <template v-if="auth.loggedIn">
          <v-list-item :to="{ name: 'my-playlists' }" title="Playlists" prepend-icon="mdi-playlist-music" link />
        </template>

        <v-list-subheader class="mt-2">Analytics</v-list-subheader>
        <v-list-item :to="{ name: 'most-played' }" title="Most Played Songs" prepend-icon="mdi-fire" link />
        <v-list-item :to="{ name: 'user-playtime' }" title="User Playtime" prepend-icon="mdi-clock-outline" link />
        <v-list-item :to="{ name: 'popular-playlists' }" title="Popular Playlists" prepend-icon="mdi-music-box-multiple" link />

        <v-list-subheader class="mt-2">Project</v-list-subheader>
        <v-list-item :to="{ name: 'about' }" title="About" prepend-icon="mdi-information-outline" link />
      </v-list>
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
  drawer.value = !display.smAndDown.value
})

watch(isDark, (val) => {
  theme.global.name.value = val ? 'dark' : 'light'
  localStorage.setItem('isDark', String(val))
})

// Adjust drawer behavior when screen size changes
watch(() => display.smAndDown.value, (isSmall) => {
  drawer.value = !isSmall
})
</script>

<style scoped>
.app-bar {
  backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.brand-title {
  font-weight: 700;
  letter-spacing: -0.02em;
}

.auth-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-drawer :deep(.v-list-item--active) {
  background: rgba(var(--v-theme-primary), 0.18);
  border-left: 3px solid rgb(var(--v-theme-primary));
}

.nav-drawer :deep(.v-list-subheader) {
  font-size: 0.75rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}
</style>
