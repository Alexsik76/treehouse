<script setup lang="ts">
// Main layout can go here (AppBar, Navigation)
</script>

<template>
  <v-app>
    <v-app-bar title="Treehouse 🌳" color="primary"> </v-app-bar>

    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>
