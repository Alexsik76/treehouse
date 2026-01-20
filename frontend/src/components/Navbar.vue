<script setup lang="ts">
import { useRouter } from "vue-router";

const router = useRouter();

const navigateTo = (name: string) => {
  router.push({ name });
};
</script>

<template>
  <v-app-bar color="primary" density="compact">
    <template v-slot:prepend>
      <v-app-bar-nav-icon icon="mdi-menu" variant="text"></v-app-bar-nav-icon>
    </template>

    <v-app-bar-title class="cursor-pointer" @click="navigateTo('home')"
      >Treehouse 🌳</v-app-bar-title
    >

    <v-spacer></v-spacer>

    <v-btn variant="text" @click="navigateTo('home')">Home</v-btn>
    <v-btn variant="text" @click="navigateTo('tree')">Tree</v-btn>
    <v-btn variant="text" @click="navigateTo('about')">About</v-btn>

    <v-divider vertical inset class="mx-2"></v-divider>

    <v-btn icon @click="navigateTo('settings')">
      <v-icon>mdi-cog</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}
</style>
