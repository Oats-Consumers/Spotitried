<template>
  <v-container>
    <h1>Popular Playlists</h1>
    <p class="mb-2">This page will list the most followed user-created playlists.</p>

    <v-data-table
      :headers="headers"
      :items="playlists"
      class="elevation-1"
      :items-per-page="5"
      :loading="loading"
      loading-text="Loading playlists..."
      hover
    >
      <template v-slot:item="{ item }">
        <tr @click="openPlaylist(item)" class="v-data-table__tr cursor-pointer">
          <td>{{ item.name }}</td>
          <td>{{ item.creator }}</td>
          <td>{{ item.followers }}</td>
        </tr>
      </template>
    </v-data-table>

    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title class="mx-auto d-inline-block pb-1 pt-4">
          Songs in {{ selectedPlaylist?.name || '' }}
        </v-card-title>
        <v-card-text class="py-0">
          <v-list class="py-0">
            <v-list-item
              class="pt-0"
              v-for="(song, index) in selectedPlaylist?.songs || []"
              :key="index"
              :title="song.title + ' - ' + song.artist"
              :subtitle="`Album: ${song.album} | Duration: ${formatDuration(song.duration)}`"
            />
            <v-list-item v-if="songsLoading" class="d-flex justify-center">
              <v-progress-circular
                indeterminate
                color="primary"
                class="my-4"
              />
            </v-list-item>
            <v-list-item v-else-if="(selectedPlaylist?.songs || []).length === 0" 
              title="No songs available." />
          </v-list>
        </v-card-text>
        <v-card-actions class="py-0">
          <v-spacer />
          <v-btn text @click="dialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Song {
  title: string
  artist: string
  album: string
  duration: number // seconds
}

interface Playlist {
  id: number
  name: string
  creator: string
  followers: number
  songs: Song[] | null // null means not loaded yet
}

const headers = [
  { title: 'Name', value: 'name' },
  { title: 'Creator', value: 'creator' },
  { title: 'Followers', value: 'followers' }
]

const playlists = ref<Playlist[]>([])
const loading = ref(true)

const selectedPlaylist = ref<Playlist | null>(null)
const dialog = ref(false)
const songsLoading = ref(false)

function formatDuration(seconds: number) {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

async function openPlaylist(playlist: Playlist) {
  selectedPlaylist.value = playlist
  dialog.value = true

  // If songs already loaded, don't fetch again
  if (playlist.songs !== null) return

  songsLoading.value = true
  try {
    const response = await fetch(`https://spotitried.onrender.com/playlist/get/${playlist.id}/songs`)
    const data = await response.json()

    playlist.songs = data.map((item: any) => ({
      title: item.title,
      artist: item.artist,
      album: item.album,
      duration: item.duration
    }))
  } catch (error) {
    console.error('Failed to fetch songs:', error)
    playlist.songs = [] // prevent retrying every time if failed
  } finally {
    songsLoading.value = false
  }
}

async function fetchPlaylists() {
  try {
    const response = await fetch('https://spotitried.onrender.com/analytics/top-playlists')
    const data = await response.json()

    playlists.value = data.map((item: any) => ({
      id: item.id,
      name: item.name,
      creator: item.created_by,
      followers: item.follower_count,
      songs: null
    }))
  } catch (error) {
    console.error('Failed to fetch playlists:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchPlaylists()
})
</script>
