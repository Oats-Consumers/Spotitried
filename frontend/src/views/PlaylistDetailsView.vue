<template>
  <v-container class="my-5">
    <h1>{{ playlist?.name }}</h1>
    <div v-if="!loading" class="text-subtitle-1 mb-4">
    Created by {{ playlist?.creator }} · {{ playlist?.followers }} followers
    </div>

    <v-list class="pt-0">
    <v-list-item
        v-for="(song, index) in songs"
        :key="song.id"
        :class="[songRowClass, 'song-row']"
        @mouseenter="hovered = index"
        @mouseleave="hovered = null"
    >
        <template #prepend>
        <div class="relative-index mr-2">
            <v-icon
            v-if="currentSong?.id === song.id"
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
            {{ index + 1 }}
            </span>
        </div>

        <v-img
            :src="song.image_url"
            alt="Song Image"
            width="40"
            height="40"
            class="rounded-square mr-2"
            cover
        />
        </template>

        <v-list-item-title>{{ song.title }} - {{ song.artist }}</v-list-item-title>
        <v-list-item-subtitle>
        Album: {{ song.album || 'Unknown' }} | Duration: {{ formatDuration(song.duration) }}
        </v-list-item-subtitle>
    </v-list-item>

    <v-list-item v-if="loading" class="d-flex justify-center">
        <v-progress-circular indeterminate />
    </v-list-item>

    <v-list-item
        v-else-if="songs.length === 0"
        class="text-center mt-10"
        title="No songs in this playlist."
    />
    </v-list>

  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useMusicPlayerStore } from '@/stores/musicPlayer'
import { useTheme } from 'vuetify'

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
}

const route = useRoute()
const playlist = ref<Playlist | null>(null)
const songs = ref<Song[]>([])
const loading = ref(true)
const hovered = ref<number | null>(null)

const playerStore = useMusicPlayerStore()
const currentSong = computed(() => playerStore.currentSong)

const theme = useTheme()
const songRowClass = computed(() =>
  theme.global.name.value === 'dark' ? 'song-row-dark' : 'song-row-light'
)

function formatDuration(seconds: number) {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

async function fetchPlaylistDetails() {
  const id = route.params.id
  try {
    const [infoRes, songsRes] = await Promise.all([
      fetch(`https://spotitried.onrender.com/playlist/by_id/${id}`),
      fetch(`https://spotitried.onrender.com/playlist/get/${id}/songs`)
    ])

    const info = await infoRes.json()
    playlist.value = {
      id: info.id,
      name: info.name,
      creator: info.created_by,
      followers: info.followers
    }

    const songList = await songsRes.json()
    songs.value = songList.map((s: any) => ({
      ...s,
      url: s.url,
      image_url: s.image_url
    }))
  } catch (err) {
    console.error('Failed to load playlist:', err)
  } finally {
    loading.value = false
  }
}

function playSong(index: number) {
  playerStore.loadPlaylist(songs.value, index)
}

onMounted(() => {
  fetchPlaylistDetails()
})
</script>

<style scoped>
.rounded-square {
  border-radius: 8px;
}

.song-row {
  transition: background-color 0.2s;
  cursor: pointer;
}

.song-row-light:hover {
  background-color: #f5f5f5;
}

.song-row-dark:hover {
  background-color: #333;
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
