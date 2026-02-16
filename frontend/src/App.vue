<script setup lang="ts">
import Navbar from "@/components/Navbar.vue";
import SideNavigation from "@/components/SideNavigation.vue";
</script>

<template>
  <v-app>
    <SideNavigation />
    <Navbar />

    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>
