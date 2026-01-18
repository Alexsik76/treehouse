<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { fetchInfrastructureItemById } from "@/services/api";
import type { InfrastructureItem } from "@/types/infrastructure";

const route = useRoute();
const router = useRouter();
const item = ref<InfrastructureItem | null>(null);
const loading = ref(true);
const error = ref<string | null>(null);

const loadItem = async () => {
  loading.value = true;
  error.value = null;
  const id = Number(route.params.id);

  if (!id) {
    error.value = "Invalid ID";
    loading.value = false;
    return;
  }

  try {
    item.value = await fetchInfrastructureItemById(id);
  } catch (e: any) {
    error.value = "Failed to load item. It may not exist.";
    console.error(e);
  } finally {
    loading.value = false;
  }
};

onMounted(loadItem);
</script>

<template>
  <v-container>
    <v-btn
      variant="text"
      icon="mdi-arrow-left"
      @click="router.back()"
      class="mb-4"
    ></v-btn>

    <div v-if="loading" class="d-flex justify-center">
      <v-progress-circular indeterminate></v-progress-circular>
    </div>

    <div v-else-if="error">
      <v-alert type="error">{{ error }}</v-alert>
    </div>

    <v-card v-else-if="item" class="mx-auto" max-width="800">
      <v-card-item>
        <template v-slot:prepend>
          <v-icon size="x-large" color="primary">mdi-server-network</v-icon>
        </template>
        <v-card-title class="text-h4">
          {{ item.name }}
        </v-card-title>
        <v-card-subtitle class="text-h6 text-high-emphasis opacity-70">
          {{ item.type }}
        </v-card-subtitle>
      </v-card-item>

      <v-divider></v-divider>

      <v-card-text class="pa-6">
        <v-row>
          <v-col cols="12" md="6">
            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="info">mdi-ip-network</v-icon>
              </template>
              <v-list-item-title>IP Address</v-list-item-title>
              <v-list-item-subtitle class="text-body-1 text-high-emphasis">
                {{ item.ip_address || "Not set" }}
              </v-list-item-subtitle>
            </v-list-item>
          </v-col>
          <v-col cols="12" md="6">
            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="purple">mdi-domain</v-icon>
              </template>
              <v-list-item-title>DNS Name</v-list-item-title>
              <v-list-item-subtitle class="text-body-1 text-high-emphasis">
                {{ item.dns_name || "Not set" }}
              </v-list-item-subtitle>
            </v-list-item>
          </v-col>
        </v-row>

        <v-divider class="my-4"></v-divider>

        <div class="text-h6 mb-2">Specifications</div>
        <v-row v-if="Object.keys(item.specs).length">
          <v-col cols="12" sm="6" v-for="(value, key) in item.specs" :key="key">
            <v-card variant="tonal" class="pa-2">
              <div
                class="text-caption text-medium-emphasis text-uppercase font-weight-bold"
              >
                {{ key }}
              </div>
              <div class="text-body-1">{{ value }}</div>
            </v-card>
          </v-col>
        </v-row>
        <div v-else class="text-caption text-medium-emphasis">
          No specifications available.
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>
