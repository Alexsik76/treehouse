<script setup lang="ts">
defineProps<{
  specs: Record<string, any>;
}>();
</script>

<template>
  <div class="text-h6 mb-2">Specifications</div>
  <v-row v-if="Object.keys(specs).length">
    <v-col cols="12" sm="6" v-for="(value, key) in specs" :key="key">
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
</template>
