<template>
  <v-container>
    <v-container class="text-center my-12">
      <v-row justify="center">
        <v-col cols="12">
          <h1 class="display-2 font-weight-bold mb-2">Welcome to Spotitried!</h1>
          <h2 class="subtitle-1 mb-4">Or at least we tried.</h2>
          <p class="mb-8">Explore your music analytics below.</p>
        </v-col>
      </v-row>
  
      <v-row justify="center" align="center" dense>
        <v-col cols="12" md="3">
          <v-card class="pa-4" elevation="2">
            <v-card-title class="justify-center">Most Played Songs</v-card-title>
            <v-card-actions class="justify-center">
              <v-btn color="primary" to="/most-played">View</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
        <v-col cols="12" md="3">
          <v-card class="pa-4" elevation="2">
            <v-card-title class="justify-center">User Playtime</v-card-title>
            <v-card-actions class="justify-center">
              <v-btn color="primary" to="/user-playtime">View</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
        <v-col cols="12" md="3">
          <v-card class="pa-4" elevation="2">
            <v-card-title class="justify-center">Popular Playlists</v-card-title>
            <v-card-actions class="justify-center">
              <v-btn color="primary" to="/popular-playlists">View</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-container>
</template>

<script setup lang="ts">
// No script needed for now
</script>
