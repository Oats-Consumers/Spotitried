import { defineStore } from 'pinia'

interface Song {
  id: number 
  title: string
  artist: string
  album: string | null
  duration: number
  image_url: string
  url: string
}

export const useMusicPlayerStore = defineStore('musicPlayer', {
  state: () => ({
    playlist: [] as Song[],
    currentIndex: -1,  // -1 = nothing selected
    playing: false
  }),
  getters: {
    currentSong(state): Song | null {
      return state.playlist[state.currentIndex] || null
    }
  },
  actions: {
    loadPlaylist(songs: Song[], startIndex = 0) {
      this.playlist = songs
      this.currentIndex = startIndex
      this.playing = true
    },
    playSongAt(index: number) {
      if (index >= 0 && index < this.playlist.length) {
        this.currentIndex = index
        this.playing = true
      }
    },
    togglePlayPause() {
      if (this.currentIndex !== -1) {
        this.playing = !this.playing
      }
    },
    playNext() {
      if (this.currentIndex < this.playlist.length - 1) {
        this.currentIndex++
        this.playing = true
      }
    },
    playPrevious() {
      if (this.currentIndex > 0) {
        this.currentIndex--
        this.playing = true
      }
    },
    stop() {
      this.playing = false
      this.currentIndex = -1
    }
  }
})
