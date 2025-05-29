<template>
  <v-container class="my-5">
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
      :items="filteredUsersWithDuration"
      class="elevation-1"
      v-model:page="page"
      v-model:items-per-page="itemsPerPage"
      :loading="loading"
      loading-text="Loading users..."
      hover
    >
      <template v-slot:item="{ item }">
        <tr>
          <td class="text-center" style="width: 40px;">{{ item.rank }}</td>
          <td>{{ item.username }}</td>
          <td>{{ item.formattedPlaytime }}</td>
        </tr>
      </template>
    </v-data-table>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { DataTableHeader } from 'vuetify'

interface UserPlaytime {
  username: string
  totalPlaytimeSeconds: number
  rank: number
}

const users = ref<UserPlaytime[]>([])
const loading = ref(true)
const search = ref('')
const page = ref(1)
const itemsPerPage = ref(5)

const headers: DataTableHeader[] = [
  { title: '#', value: 'rank', align: 'center' },
  { title: 'Username', value: 'username' },
  { title: 'Total Playtime', value: 'formattedPlaytime' }
]

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

const filteredUsersWithDuration = computed(() =>
  filteredUsers.value.map(user => ({
    ...user,
    formattedPlaytime: formatDuration(user.totalPlaytimeSeconds)
  }))
)

async function fetchUserPlaytime() {
  try {
    const response = await fetch('https://spotitried.onrender.com/analytics/user-playtime')
    const data = await response.json()

    users.value = data
      .sort((a: any, b: any) => b.total_playtime - a.total_playtime)
      .map((item: any, index: number) => ({
        username: item.username,
        totalPlaytimeSeconds: item.total_playtime,
        rank: index + 1
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