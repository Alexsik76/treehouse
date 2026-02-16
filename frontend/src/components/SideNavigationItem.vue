<script setup lang="ts">
import { computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import type { InfrastructureItem } from "@/types/infrastructure";

const props = defineProps<{
  item: InfrastructureItem;
}>();

const router = useRouter();
const route = useRoute();

const visibleChildren = computed(() => {
  if (!props.item.children) return [];
  // Filter out nested servers as per user request
  return props.item.children.filter((child) => child.type !== "server");
});

const hasChildren = computed(() => visibleChildren.value.length > 0);
const isActive = computed(() => Number(route.params.id) === props.item.id);

const typeIcon = computed(() => {
  switch (props.item.type) {
    case "server":
      return "mdi-server";
    case "vm":
      return "mdi-desktop-tower";
    case "container":
      return "mdi-docker";
    default:
      return "mdi-help-circle-outline";
  }
});

const navigate = () => {
  router.push({
    name: "server-details",
    params: { id: props.item.id },
  });
};
</script>

<template>
  <v-list-group v-if="hasChildren" :value="item.id">
    <template v-slot:activator="{ props, isOpen }">
      <v-list-item :title="item.name" :active="isActive" @click="navigate">
        <template v-slot:prepend>
          <v-icon :icon="typeIcon" :title="item.type"></v-icon>
        </template>

        <template v-slot:append>
          <!-- Expand Button -->
          <v-btn
            icon
            variant="text"
            size="small"
            :ripple="false"
            class="sidebar-expand-btn"
            v-bind="props"
            @click.stop
          >
            <v-icon
              :icon="isOpen ? 'mdi-chevron-up' : 'mdi-chevron-down'"
            ></v-icon>
          </v-btn>
        </template>
      </v-list-item>
    </template>

    <SideNavigationItem
      v-for="child in visibleChildren"
      :key="child.id"
      :item="child"
    />
  </v-list-group>

  <!-- Leaf Item -->
  <v-list-item
    v-else
    :title="item.name"
    :value="item.id"
    :active="isActive"
    @click="navigate"
  >
    <template v-slot:prepend>
      <v-icon :icon="typeIcon" :title="item.type"></v-icon>
    </template>
  </v-list-item>
</template>

<style scoped>
/* 
   Aggressively remove all focus indicators including browser defaults and Vuetify overlays.
   The goal is to prevent the "sticky" white circle after clicking.
*/
.sidebar-expand-btn:focus {
  outline: none !important;
  box-shadow: none !important;
}

.sidebar-expand-btn:focus-visible {
  outline: none !important;
}

/* Remove the overlay background when the button is FOCUSED but NOT hovered. */
.sidebar-expand-btn:focus:not(:hover) :deep(.v-btn__overlay) {
  opacity: 0 !important;
}

/* Also ensure ::before/::after pseudo-elements don't show focus rings */
.sidebar-expand-btn:focus::before,
.sidebar-expand-btn:focus::after {
  opacity: 0 !important;
}
</style>
