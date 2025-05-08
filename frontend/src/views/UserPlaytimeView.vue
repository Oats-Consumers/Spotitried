<template>
  <v-container>
    <h1>User Playtime</h1>
    <p class="mb-2">This page will show total playtime for each user last month.</p>

    <v-text-field
      v-model="search"
      label="Search by username"
      prepend-inner-icon="mdi-magnify"
      clearable
    />

    <v-data-table
      :headers="headers"
      :items="filteredUsers.map(user => ({
        ...user,
        formattedPlaytime: formatDuration(user.totalPlaytimeSeconds)
      }))"
      class="elevation-1"
      :items-per-page="5"
      :loading="loading"
      loading-text="Loading users..."
      hover
    >
      <template v-slot:item="{ item }">
        <tr>
          <td class="text-center" style="width: 40px;">{{ item.index }}</td>
          <td>{{ item.username }}</td>
          <td>{{ item.formattedPlaytime }}</td>
        </tr>
      </template>
    </v-data-table>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

interface UserPlaytime {
  username: string
  totalPlaytimeSeconds: number
}

const users = ref<UserPlaytime[]>([])
const loading = ref(true)

const headers = [
  { title: '#', value: 'index', align: 'center' },
  { title: 'Username', value: 'username' },
  { title: 'Total Playtime', value: 'formattedPlaytime' }
]

const search = ref('')

function formatDuration(seconds: number) {
  const hours = Math.floor(seconds / 3600)
  const mins = Math.floor((seconds % 3600) / 60)
  return `${hours}h ${mins}m`
}

const filteredUsers = computed(() => {
  if (!search.value) return users.value
  return users.value.filter(user => 
    user.username.toLowerCase().includes(search.value.toLowerCase())
  )
})

async function fetchUserPlaytime() {
  try {
    const response = await fetch('https://spotitried.onrender.com/analytics/user-playtime')
    const data = await response.json()

    users.value = data.map((item: any, index: number) => ({
      index: index + 1,
      username: item.username,
      totalPlaytimeSeconds: item.total_playtime
    }))
  } catch (error) {
    console.error('Failed to fetch user playtime:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchUserPlaytime()
})
</script>

<style scoped>
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