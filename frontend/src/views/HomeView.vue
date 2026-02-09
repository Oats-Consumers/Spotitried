<template>
  <v-container class="home-view">
    <section class="home-hero">
      <v-row align="center">
        <v-col cols="12" md="7">
          <p class="eyebrow">Your Listening Story</p>
          <h1 class="hero-title">Welcome to Spotitried.</h1>
          <p class="hero-subtitle">Or at least we tried. Track your top tracks, playlist trends, and time spent listening.</p>
          <div class="hero-actions">
            <v-btn color="primary" size="large" to="/most-played">Explore Most Played</v-btn>
            <v-btn variant="tonal" color="secondary" size="large" to="/user-playtime">Check Playtime</v-btn>
          </div>
        </v-col>
        <v-col cols="12" md="5">
          <v-card class="hero-card" elevation="8">
            <v-card-title>Quick Insights</v-card-title>
            <v-card-text>
              <ul class="hero-list">
                <li>Find your most replayed tracks in seconds.</li>
                <li>See how your listening time stacks up.</li>
                <li>Discover playlists trending across users.</li>
              </ul>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </section>

    <section class="home-cards">
      <v-row justify="center" align="stretch">
        <v-col cols="12" md="4">
          <v-card class="feature-card" elevation="6">
            <v-card-title>
              <v-icon class="mr-2" icon="mdi-fire" />
              Most Played Songs
            </v-card-title>
            <v-card-text>Surface your hottest tracks and the artists you keep on repeat.</v-card-text>
            <v-card-actions>
              <v-btn color="primary" variant="text" to="/most-played">View Rankings</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <v-card class="feature-card" elevation="6">
            <v-card-title>
              <v-icon class="mr-2" icon="mdi-clock-outline" />
              User Playtime
            </v-card-title>
            <v-card-text>Track listening minutes and see when you are most active.</v-card-text>
            <v-card-actions>
              <v-btn color="primary" variant="text" to="/user-playtime">View Activity</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <v-card class="feature-card" elevation="6">
            <v-card-title>
              <v-icon class="mr-2" icon="mdi-music-box-multiple" />
              Popular Playlists
            </v-card-title>
            <v-card-text>Browse playlists other listeners cannot stop sharing.</v-card-text>
            <v-card-actions>
              <v-btn color="primary" variant="text" to="/popular-playlists">Browse Playlists</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </section>
  </v-container>
</template>

<script setup lang="ts"></script>

<style scoped>
.home-view {
  padding-top: 40px;
  padding-bottom: 60px;
}

.home-hero {
  padding: 24px 0 40px;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.2em;
  font-size: 0.75rem;
  margin-bottom: 12px;
  color: rgba(var(--v-theme-primary), 0.9);
}

.hero-title {
  font-size: clamp(2.5rem, 4vw, 3.5rem);
  line-height: 1.05;
  margin-bottom: 12px;
}

.hero-subtitle {
  font-size: 1.1rem;
  max-width: 520px;
  margin-bottom: 24px;
  color: rgba(var(--v-theme-on-surface), 0.75);
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.hero-card {
  border-radius: 18px;
  background: linear-gradient(140deg, rgba(var(--v-theme-primary), 0.18), rgba(var(--v-theme-secondary), 0.1));
}

.hero-list {
  padding-left: 18px;
  margin: 0;
  display: grid;
  gap: 10px;
}

.home-cards {
  margin-top: 24px;
}

.feature-card {
  height: 100%;
  border-radius: 18px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 30px rgba(0, 0, 0, 0.18);
}
</style>
