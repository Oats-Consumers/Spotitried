<template>
  <v-footer
    app
    v-if="player.currentSong"
    class="d-flex flex-column px-4 py-2 justify-center"
  >
    <!-- ───── Top row: song info and controls ───── -->
    <div class="d-flex align-center justify-space-between w-100">
      <div class="d-flex align-center">
        <v-img
          :src="player.currentSong.image_url"
          alt="Song Image"
          height="48"
          width="48"
          class="rounded-square mr-2"
          cover
        />
        <div>
          <div>{{ player.currentSong.title }}</div>
          <small class="text-grey">{{ player.currentSong.artist }}</small>
        </div>
      </div>

      <div class="d-flex align-center">
        <v-btn icon @click="playPrevious" :disabled="player.currentIndex <= 0">
          <v-icon>mdi-skip-previous</v-icon>
        </v-btn>
        <v-btn icon @click="togglePlay" class="mx-2">
          <v-icon>{{ player.playing ? 'mdi-pause' : 'mdi-play' }}</v-icon>
        </v-btn>
      <v-btn icon @click="playNext" :disabled="player.currentIndex >= player.playlist.length - 1">
          <v-icon>mdi-skip-next</v-icon>
        </v-btn>
      </div>
    </div>

    <!-- ───── Bottom row: progress bar ───── -->
    <div class="progress-bar-container">
      <div class="time-labels">
        <small>{{ formatTime(currentTime) }}</small>
        <small>{{ formatTime(duration) }}</small>
      </div>
      <div class="progress-track" @click="seekTo">
        <div
          class="progress-fill"
          :style="{ width: ((currentTime / duration) * 100 || 0) + '%' }"
        />
      </div>
    </div>
  </v-footer>

  <audio
    ref="audio"
    style="display: none"
    :src="player.currentSong?.url ?? ''"
    preload="metadata"
    @ended="onEnded"
  />
</template>

<script setup lang="ts">
import { ref, watch, nextTick, onBeforeUnmount } from 'vue'
import { useMusicPlayerStore } from '@/stores/musicPlayer'
import { useAuthStore } from '@/stores/auth'

const player = useMusicPlayerStore()
const auth = useAuthStore()

const audio = ref<HTMLAudioElement | null>(null)

const currentTime = ref(0)
const duration = ref(0)

let timer: ReturnType<typeof setInterval> | null = null
let playbackStart: number | null = null

function updateTime() {
  if (audio.value) {
    currentTime.value = audio.value.currentTime
    duration.value = audio.value.duration || 0
  }
}

function seekTo(e: Event) {
  const bar = e.currentTarget as HTMLElement
  const rect = bar.getBoundingClientRect()
  const clickX = (e as MouseEvent).clientX - rect.left
  const percent = clickX / rect.width
  if (audio.value) {
    audio.value.currentTime = percent * (audio.value.duration || 0)
    updateTime()
  }
}

function formatTime(seconds: number) {
  const min = Math.floor(seconds / 60)
  const sec = Math.floor(seconds % 60)
  return `${min}:${sec.toString().padStart(2, '0')}`
}

function startTimer() {
  stopTimer()
  updateTime()
  timer = setInterval(updateTime, 500)
  playbackStart = Date.now()
}

function stopTimer(report = true) {
  if (timer) {
    clearInterval(timer)
    timer = null
  }

  if (report && playbackStart && player.currentSong && auth.id) {
    const durationPlayed = Math.floor((Date.now() - playbackStart) / 1000)
    if (durationPlayed >= 3) {
      fetch('https://spotitried.onrender.com/basic/playback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          listener_id: auth.id,
          song_id: player.currentSong.id,
          duration_played: durationPlayed
        })
      }).catch(console.error)
    }
  }

  playbackStart = null
}

// ─── Watch song changes ───
watch(
  () => player.currentSong,
  async (song) => {
    stopTimer()

    if (!song) return
    await nextTick()
    if (!audio.value) return

    audio.value.src = song.url
    audio.value.load()

    if (player.playing) {
      audio.value.play().catch(() => {})
      startTimer()
    }
  },
  { flush: 'post' }
)

// ─── Watch play/pause state ───
watch(
  () => player.playing,
  async (isPlaying) => {
    await nextTick()
    if (!audio.value) return

    if (isPlaying) {
      audio.value.play().catch(() => {})
      startTimer()
    } else {
      audio.value.pause()
      stopTimer()
    }
  },
  { flush: 'post', immediate: true }
)

function togglePlay() {
  player.playing = !player.playing
}
function playNext() {
  stopTimer()
  player.playNext()
}
function playPrevious() {
  stopTimer()
  player.playPrevious()
}
function onEnded() {
  stopTimer()
  player.playNext()
}

// Clean up when tab is closed
onBeforeUnmount(() => {
  stopTimer()
})
</script>

<style scoped>
.rounded-square {
  border-radius: 8px;
}

.progress-bar-container {
  width: 100%;
  display: flex;
  flex-direction: column;
}

.time-labels {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #aaa;
  padding: 0 4px;
}

.progress-track {
  position: relative;
  height: 4px;
  background-color: #555;
  cursor: pointer;
  border-radius: 2px;
  margin-top: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #0ec444; /* Spotify green */
  transition: width 0.2s;
}
</style>
