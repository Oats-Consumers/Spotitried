<template>
  <v-container>
    <h1>Popular Playlists</h1>
    <p class="mb-2">This page will list the most followed user-created playlists.</p>

    <v-data-table
      :headers="headers"
      :items="playlists.map((item, index) => ({ ...item, index: index + 1 }))"
      class="elevation-1"
      :items-per-page="5"
      :loading="loading"
      loading-text="Loading playlists..."
      hover
    >
      <template v-slot:item="{ item }">
        <tr @click="openPlaylist(item)" class="v-data-table__tr cursor-pointer">
          <td class="text-center" style="width: 40px;">{{ item.index }}</td>
          <td>{{ item.name }}</td>
          <td>{{ item.creator }}</td>
          <td>{{ item.followers }}</td>
        </tr>
      </template>
    </v-data-table>

    <v-dialog v-model="dialog" max-width="700px">
      <v-card>
        <v-card-title class="mx-auto d-inline-block pb-1 pt-4">
          Songs in {{ selectedPlaylist?.name || '' }}
        </v-card-title>
        <v-card-text class="py-0">
          <v-list class="py-0">
            <v-list-item
              v-for="(song, index) in selectedPlaylist?.songs || []"
              :key="index"
              class="song-row"
              @mouseenter="hoveredIndex = index"
              @mouseleave="hoveredIndex = null"
            >
              <template #prepend>
                <v-icon
                  v-if="hoveredIndex === index"
                  size="20"
                  @click.stop="playSong(index)"
                  class="fade-in mr-2"
                >
                  mdi-play
                </v-icon>
                <span 
                  v-else 
                  class="mr-2 text-center fade-out" 
                  style="width: 20px;"
                >{{ index + 1 }}</span>

                <v-img 
                  :src="song.image_url" 
                  alt="Song Image" 
                  height="40" 
                  width="40"
                  class="rounded-square mr-2"
                  cover
                />
              </template>
              <v-list-item-title>{{ song.title }} - {{ song.artist }}</v-list-item-title>
              <v-list-item-subtitle>
                Album: {{ song.album || 'Unknown' }} | Duration: {{ formatDuration(song.duration) }}
              </v-list-item-subtitle>
            </v-list-item>

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
import { useMusicPlayerStore } from '@/stores/musicPlayer'

interface Song {
  id: number
  title: string
  artist: string
  album: string | null
  duration: number
  url: string
  image_url: string
}

interface Playlist {
  id: number
  name: string
  creator: string
  followers: number
  songs: Song[] | null
}

const headers = [
  { title: '#', value: 'index', align: 'center' },
  { title: 'Name', value: 'name' },
  { title: 'Creator', value: 'creator' },
  { title: 'Followers', value: 'followers' }
]

const playlists = ref<Playlist[]>([])
const loading = ref(true)

const selectedPlaylist = ref<Playlist | null>(null)
const dialog = ref(false)
const songsLoading = ref(false)

const hoveredIndex = ref<number | null>(null)

function formatDuration(seconds: number) {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

async function openPlaylist(playlist: Playlist) {
  selectedPlaylist.value = playlist
  dialog.value = true

  if (playlist.songs !== null) return

  songsLoading.value = true
  try {
    const response = await fetch(`https://spotitried.onrender.com/playlist/get/${playlist.id}/songs`)
    const data = await response.json()

    playlist.songs = data.map((item: any) => ({
      id: item.id,
      title: item.title,
      artist: item.artist,
      album: item.album,
      duration: item.duration,
      url: item.url,
      image_url: item.image_url
    }))
  } catch (error) {
    console.error('Failed to fetch songs:', error)
    playlist.songs = []
  } finally {
    songsLoading.value = false
  }
}

function playSong(index: number) {
  if (!selectedPlaylist.value) return
  const player = useMusicPlayerStore()
  player.loadPlaylist(selectedPlaylist.value.songs!, index)
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

<style scoped>
.rounded-square {
  border-radius: 8px;
}

.song-row {
  transition: background-color 0.2s;
}

.song-row:hover {
  background-color: #f5f5f5;
  cursor: pointer;
}

::v-deep(th:first-child) {
  padding-right: 0 !important;
  text-align: center;
  width: 40px;
}

td:first-child {
  padding-right: 0 !important;
  text-align: center;
  width: 40px;
}

.fade-in {
  opacity: 1;
  transition: opacity 0.2s;
}

.fade-out {
  opacity: 1;
  transition: opacity 0.2s;
}

.song-row:hover .fade-out {
  opacity: 0;
}
</style>