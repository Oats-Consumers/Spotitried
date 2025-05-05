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
        <v-card-text class="pt-0">
          <v-list class="pt-0">
            <v-list-item
              class="pt-0"
              v-for="(song, index) in selectedPlaylist?.songs || []"
              :key="index"
              :title="song.title + ' - ' + song.artist"
              :subtitle="`Album: ${song.album} | Duration: ${formatDuration(song.duration)}`"
            />
            <v-list-item v-if="(selectedPlaylist?.songs || []).length === 0" title="No songs available." />
          </v-list>
        </v-card-text>
        <v-card-actions>
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
  name: string
  creator: string
  followers: number
  songs: Song[]
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

function openPlaylist(playlist: Playlist) {
  selectedPlaylist.value = playlist
  dialog.value = true
}

function formatDuration(seconds: number) {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

async function fetchPlaylists() {
  try {
    const response = await fetch('https://spotitried.onrender.com/analytics/top-playlists')
    const data = await response.json()

    playlists.value = data.map((item: any) => ({
      name: item.name,
      creator: item.created_by,
      followers: item.follower_count,
      songs: [] // API doesn't provide songs, so leave empty
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
