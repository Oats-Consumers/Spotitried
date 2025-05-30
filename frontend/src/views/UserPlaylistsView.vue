<template>
  <v-container class="my-5">
    <v-row class="mb-4 d-flex align-center">
      <h1>My Playlists</h1>
      <v-spacer></v-spacer>
      <v-switch
        v-model="showOnlyCreated"
        label="Show only my playlists"
        class="d-flex align-center mr-3"
      />
      <!-- Create Playlist Button -->
      <v-btn color="primary" class="align-center" @click="showDialog = true">
        Create New Playlist
      </v-btn>
    </v-row>


    <!-- Playlist Cards -->
    <v-row>
      <v-col
        v-for="playlist in filteredPlaylists"
        :key="playlist.id"
        cols="12"
        sm="6"
        md="4"
      >
        <v-card class="mx-auto" outlined @click="goToPlaylist(playlist.id)" hover>
          <v-card-title>{{ playlist.name }}</v-card-title>
          <v-card-subtitle>Followers: {{ playlist.follower_count }}</v-card-subtitle>
          <v-card-text class="text-right">Created by {{ playlist.created_by }}</v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Empty State -->
    <v-alert
      v-if="!playlists.length && !loading"
      type="info"
      variant="tonal"
      class="mt-4"
    >
      You haven't created or followed any playlists yet.
    </v-alert>

    <!-- Loading State -->
    <v-skeleton-loader v-if="loading" type="card" class="mt-4" />

    <!-- Create Playlist Dialog -->
    <v-dialog v-model="showDialog" max-width="400">
      <v-card>
        <v-card-title>Create Playlist</v-card-title>
        <v-card-text class="py-0">
          <v-text-field
            v-model="newPlaylistName"
            label="Playlist Name"
            :rules="[v => !!v || 'Name is required']"
            required
            hide-details="auto"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="showDialog = false">Cancel</v-btn>
          <v-btn
            color="primary"
            @click="createPlaylist"
            :disabled="!newPlaylistName || creating"
          >
            <v-progress-circular
              v-if="creating"
              indeterminate
              size="20"
              class="mr-2"
            />
            <div v-else>
              Create
            </div>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

interface Playlist {
  id: number
  name: string
  created_by: string
  follower_count: number
}

const playlists = ref<Playlist[]>([])
const loading = ref(true)
const creating = ref(false)
const showDialog = ref(false)
const newPlaylistName = ref('')
const auth = useAuthStore()
const router = useRouter()
const showOnlyCreated = ref(false)

const fetchMyPlaylists = async () => {
  if (!auth.loggedIn || !auth.id) return

  loading.value = true
  try {
    const res = await fetch(`https://spotitried.onrender.com/analytics/listener-playlist-follows/${auth.id}`)
    const data = await res.json()
    playlists.value = data
  } catch (err) {
    console.error('Failed to fetch playlists:', err)
  } finally {
    loading.value = false
  }
}

const filteredPlaylists = computed(() =>
  showOnlyCreated.value
    ? playlists.value.filter(p => p.created_by === auth.username)
    : playlists.value
)

const goToPlaylist = (id: number) => {
  router.push({ name: 'playlist-details', params: { id } })
}

const createPlaylist = async () => {
  if (!newPlaylistName.value.trim()) return
  creating.value = true

  try {
    const response = await fetch('https://spotitried.onrender.com/playlist/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: newPlaylistName.value,
        listener_id: auth.id
      })
    })

    const playlist = await response.json()

    await fetch(`https://spotitried.onrender.com/user/follow/${auth.id}/${playlist.id}`, {
      method: 'POST'
    })

    await fetchMyPlaylists()
    showDialog.value = false
  } catch (error) {
    console.error('Failed to create playlist:', error)
  } finally {
    creating.value = false
    newPlaylistName.value = ''
  }
}


onMounted(() => {
  fetchMyPlaylists()
})
</script>
