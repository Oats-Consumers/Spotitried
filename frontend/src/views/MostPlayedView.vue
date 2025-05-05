<template>
  <v-container>
    <h1>Most Played Songs</h1>
    <p class="mb-2">This page will display the most played songs in the past week.</p>

    <v-data-table
      :headers="headers"
      :items="songs.map(song => ({
        ...song,
        formattedDuration: formatDuration(song.duration)
      }))"
      class="elevation-1"
      :items-per-page="5"
      :loading="loading"
      loading-text="Loading songs..."
      hover
    />
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Song {
  title: string
  artist: string
  album: string
  duration: number // seconds
  playCount: number
}

const songs = ref<Song[]>([])
const loading = ref(true)

const headers = [
  { title: 'Title', value: 'title' },
  { title: 'Artist', value: 'artist' },
  { title: 'Album', value: 'album' },
  { title: 'Duration', value: 'formattedDuration' },
  { title: 'Play Count', value: 'playCount' }
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
      playCount: item.play_count
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
