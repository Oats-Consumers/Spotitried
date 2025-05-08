<template>
  <v-container>
    <h1>Most Played Songs</h1>
    <p class="mb-2">This page will display the most played songs in the past week.</p>

    <v-data-table
      :headers="headers"
      :items="songs.map((song, index) => ({
        ...song,
        index: index + 1,
        formattedDuration: formatDuration(song.duration)
      }))"
      class="elevation-1"
      :items-per-page="5"
      :loading="loading"
      loading-text="Loading songs..."
      hover
    >
      <template v-slot:item="{ item }">
        <tr>
          <td class="text-center" style="width: 40px;">{{ item.index }}</td>
          <td>
            <div class="d-flex align-center">
              <v-avatar size="40" class="rounded-square mr-2">
                <v-img :src="item.image_url" alt="Song Image" cover />
              </v-avatar>
              <span>{{ item.title }}</span>
            </div>
          </td>
          <td>{{ item.artist }}</td>
          <td>{{ item.album || 'Unknown' }}</td>
          <td>{{ item.formattedDuration }}</td>
          <td>{{ item.play_count }}</td>
        </tr>
      </template>
    </v-data-table>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Song {
  title: string
  artist: string
  album: string | null
  duration: number // seconds
  play_count: number
  image_url: string
}

const songs = ref<Song[]>([])
const loading = ref(true)

const headers = [
  { title: '#', value: 'index', align: 'center' },
  { title: 'Title', value: 'title' },
  { title: 'Artist', value: 'artist' },
  { title: 'Album', value: 'album' },
  { title: 'Duration', value: 'formattedDuration' },
  { title: 'Play Count', value: 'play_count' }
]

function formatDuration(seconds: number) {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

async function fetchSongs() {
  try {
    const response = await fetch('https://spotitried.onrender.com/analytics/most-played-songs')
    const data = await response.json()

    songs.value = data.map((item: any) => ({
      title: item.title,
      artist: item.artist,
      album: item.album,
      duration: item.duration,
      play_count: item.total_play_time,
      image_url: item.image_url
    }))
  } catch (error) {
    console.error('Failed to fetch songs:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchSongs()
})
</script>

<style scoped>
.rounded-square {
  border-radius: 8px; /* Slightly rounded corners like Spotify */
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
</style>
