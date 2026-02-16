<script setup lang="ts">
import { ref, watch } from "vue";
import { useRoute } from "vue-router";
import { useInfrastructure } from "@/services/api";
import SideNavigationItem from "@/components/SideNavigationItem.vue";
import type { InfrastructureItem } from "@/types/infrastructure";

const drawer = ref(true);
const route = useRoute();
const openIds = ref<number[]>([]);

const { data: items, isFetching } = useInfrastructure();

// Function to find the path to a node to expand it
const findPathToNode = (
  items: InfrastructureItem[],
  targetId: number,
  path: number[] = [],
): number[] | null => {
  for (const item of items) {
    if (item.id === targetId) {
      return [...path, item.id];
    }
    if (item.children) {
      const result = findPathToNode(item.children, targetId, [
        ...path,
        item.id,
      ]);
      if (result) return result;
    }
  }
  return null;
};

// Watch route to update openIds
watch(
  () => route.params.id,
  (newId) => {
    if (!newId || !items.value) return;
    const id = Number(newId);
    const path = findPathToNode(items.value, id);
    if (path) {
      // Add path to openIds to expand the tree to the current node
      // We use a Set to avoid duplicates
      const newOpenIds = new Set([...openIds.value, ...path]);
      openIds.value = Array.from(newOpenIds);
    }
  },
  { immediate: true, deep: true },
);

// Watch items to trigger expansion on initial load/refresh
watch(items, (newItems) => {
  if (newItems && route.params.id) {
    const id = Number(route.params.id);
    const path = findPathToNode(newItems, id);
    if (path) {
      const newOpenIds = new Set([...openIds.value, ...path]);
      openIds.value = Array.from(newOpenIds);
    }
  }
});
</script>

<template>
  <v-navigation-drawer v-model="drawer" :width="300">
    <div class="pa-4 d-flex align-center">
      <v-icon icon="mdi-server-network" class="mr-2" color="primary"></v-icon>
      <span class="text-h6 font-weight-bold">DeepTree</span>
    </div>

    <v-divider></v-divider>

    <div v-if="isFetching && !items" class="d-flex justify-center pa-4">
      <v-progress-circular indeterminate size="24"></v-progress-circular>
    </div>

    <v-list
      v-else-if="items"
      v-model:opened="openIds"
      nav
      density="compact"
      open-strategy="multiple"
    >
      <v-list-subheader
        class="text-uppercase font-weight-bold text-caption text-medium-emphasis"
      >
        Infrastructure
      </v-list-subheader>

      <SideNavigationItem v-for="item in items" :key="item.id" :item="item" />
    </v-list>
  </v-navigation-drawer>
</template>
