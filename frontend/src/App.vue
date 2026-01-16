<script setup lang="ts">
import { ref, onMounted } from 'vue'

const message = ref<string>('Connecting...')
const status = ref<string>('gray')

// Функція для перевірки зв'язку з бекендом
const checkBackend = async () => {
  try {
    // Звертаємось до локального FastAPI (порт 8000)
    const response = await fetch('http://localhost:8000/')
    const data = await response.json()
    message.value = data.message // "Welcome to the Treehouse API"
    status.value = 'success'
  } catch (error) {
    message.value = 'Error: Backend unavailable'
    status.value = 'error'
    console.error(error)
  }
}

onMounted(() => {
  checkBackend()
})
</script>

<template>
  <v-app>
    <v-app-bar title="Treehouse 🌳" color="primary"></v-app-bar>

    <v-main>
      <v-container class="fill-height justify-center">
        <v-card width="400" variant="outlined">
          <v-card-item>
            <v-card-title>System Status</v-card-title>
            <v-card-subtitle>Local Dev Environment</v-card-subtitle>
          </v-card-item>

          <v-card-text>
            <div class="text-h6 mb-2">Backend Response:</div>
            <v-alert
              :color="status === 'success' ? 'success' : 'error'"
              :icon="status === 'success' ? 'mdi-check-circle' : 'mdi-alert-circle'"
              variant="tonal"
            >
              {{ message }}
            </v-alert>
          </v-card-text>

          <v-card-actions>
            <v-btn variant="elevated" color="primary" @click="checkBackend">
              Refresh Ping
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>