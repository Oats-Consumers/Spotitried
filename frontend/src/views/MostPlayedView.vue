<template>
  <v-container class="my-5">
    <h1>Most Played Songs</h1>
    <p class="mb-2">This page will display the most played songs in the past week.</p>

    <v-data-table
      :headers="headers"
      :items="formattedSongs"
      class="elevation-1"
      :items-per-page="5"
      :loading="loading"
      loading-text="Loading songs..."
      hover
    >
      <template v-slot:item="{ item, index }">
        <tr @mouseenter="hovered = index" @mouseleave="hovered = null">
          <td class="text-center">
            <div class="relative-index mr-2">
              <v-icon
                v-if="currentSong?.id === item.id"
                class="playing-icon"
                size="20"
                color="#0ec444"
              >
                mdi-equalizer
              </v-icon>
              <v-icon
                v-else-if="hovered === index"
                class="play-icon"
                size="20"
                @click.stop="playSong(index)"
              >
                mdi-play
              </v-icon>
              <span v-else class="song-number">
                {{ item.index }}
              </span>
            </div>
          </td>
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
          <td class="text-center">{{ item.formattedDuration }}</td>
          <td class="text-center">{{ item.formattedPlayTime }}</td>
        </tr>
      </template>
    </v-data-table>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useMusicPlayerStore } from '@/stores/musicPlayer'
import type { DataTableHeader } from 'vuetify'

interface Song {
  id: number
  title: string
  artist: string
  album: string | null
  duration: number // in seconds
  total_play_time: number // in seconds
  url: string
  image_url: string
}

const songs = ref<Song[]>([])
const loading = ref(true)
const hovered = ref<number | null>(null)

const player = useMusicPlayerStore()
const currentSong = computed(() => player.currentSong)

const headers: DataTableHeader[] = [
  { title: '#', value: 'index', align: 'center' },
  { title: 'Title', value: 'title' },
  { title: 'Artist', value: 'artist' },
  { title: 'Album', value: 'album' },
  { title: 'Duration', value: 'formattedDuration', align: 'center' },
  { title: 'Total Listening Time', value: 'formattedPlayTime', align: 'center' }
]

function formatTime(seconds: number): string {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

const formattedSongs = computed(() =>
  songs.value.map((song, index) => ({
    ...song,
    index: index + 1,
    formattedDuration: formatTime(song.duration),
    formattedPlayTime: formatTime(song.total_play_time)
  }))
)

function playSong(index: number) {
  player.loadPlaylist(formattedSongs.value, index)
}

async function fetchSongs() {
  try {
    const response = await fetch('https://spotitried.onrender.com/analytics/most-played-songs')
    const data = await response.json()
    songs.value = data
  } catch (error) {
    console.error('Failed to fetch songs:', error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchSongs)
</script>

<style scoped>
.rounded-square {
  border-radius: 8px;
}

.relative-index {
  position: relative;
  width: 20px;
  height: 20px;
}

.play-icon,
.song-number,
.playing-icon {
  position: absolute;
  top: 0;
  left: 0;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

::v-deep(th:first-child),
td:first-child {
  padding-right: 0 !important;
  text-align: center;
  width: 40px;
}
</style>
