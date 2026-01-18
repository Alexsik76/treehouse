<script setup lang="ts">
import type { InfrastructureItem } from "@/types/infrastructure";

defineProps<{
  items: InfrastructureItem[];
}>();

const emit = defineEmits<{
  (e: "delete", item: InfrastructureItem): void;
  (e: "edit", item: InfrastructureItem): void;
  (e: "add-child", parentId: number): void;
}>();

// Helper icon mapping based on type
const getIcon = (type: string) => {
  switch (type) {
    case "server":
      return "mdi-server";
    case "vm":
      return "mdi-monitor";
    case "container":
      return "mdi-docker";
    case "switch":
      return "mdi-switch";
    case "router":
      return "mdi-router";
    default:
      return "mdi-cube-outline";
  }
};
</script>

<template>
  <v-list>
    <template v-for="item in items" :key="item.id">
      <!-- Vuetify List Group for collapsible children -->
      <v-list-group :value="item.name">
        <template v-slot:activator="{ props }">
          <v-list-item v-bind="props" :prepend-icon="getIcon(item.type)">
            <!-- Title with Router Link -->
            <template v-slot:title>
              <router-link
                :to="{ name: 'server-details', params: { id: item.id } }"
                class="text-decoration-none text-high-emphasis font-weight-bold server-link"
                @click.stop
                title="Click to view details"
              >
                {{ item.name }}
              </router-link>
            </template>

            <!-- Subtitle with IP and DNS -->
            <template v-slot:subtitle>
              <div class="d-flex align-center">
                <span
                  v-if="item.ip_address"
                  class="mr-2 text-body-2 text-medium-emphasis"
                >
                  {{ item.ip_address }}
                </span>
                <span
                  v-if="item.dns_name"
                  class="text-caption text-primary font-italic"
                >
                  ({{ item.dns_name }})
                </span>
                <span
                  v-if="!item.ip_address && !item.dns_name"
                  class="text-caption text-disabled"
                >
                  No Address
                </span>
              </div>
            </template>
            <template v-slot:append>
              <!-- Expansion Trigger Area -->
              <div class="d-flex align-center mr-4 text-medium-emphasis">
                <v-icon
                  v-if="item.children && item.children.length > 0"
                  icon="mdi-file-tree"
                  size="small"
                  class="mr-2"
                ></v-icon>
                <v-badge
                  v-if="item.children && item.children.length > 0"
                  :content="item.children.length"
                  color="secondary"
                  inline
                  class="mr-2"
                ></v-badge>
              </div>

              <!-- Type Chip -->
              <v-chip size="x-small" class="mr-2" color="primary">{{
                item.type
              }}</v-chip>

              <!-- Action Buttons -->
              <v-btn
                icon="mdi-plus"
                size="small"
                variant="text"
                color="success"
                @click.stop="emit('add-child', item.id)"
                title="Add Child"
              ></v-btn>
              <v-btn
                icon="mdi-pencil"
                size="small"
                variant="text"
                color="info"
                @click.stop="emit('edit', item)"
                title="Edit Item"
              ></v-btn>
              <v-btn
                icon="mdi-delete"
                size="small"
                variant="text"
                color="error"
                @click.stop="emit('delete', item)"
                title="Delete Item"
              ></v-btn>
            </template>
          </v-list-item>
        </template>

        <!-- Recursive Rendering -->
        <div class="ml-4 border-l-2 pl-2 mb-2">
          <template v-if="item.children && item.children.length > 0">
            <!-- Recursive Call: Pass down the listeners -->
            <InfrastructureTree
              :items="item.children"
              @delete="(childItem) => emit('delete', childItem)"
              @edit="(childItem) => emit('edit', childItem)"
              @add-child="(id) => emit('add-child', id)"
            />
          </template>
          <template v-else>
            <div class="pl-4 py-2 text-caption text-medium-emphasis">
              No children.
              <v-btn
                variant="text"
                size="x-small"
                color="primary"
                @click="emit('add-child', item.id)"
              >
                Add one?
              </v-btn>
            </div>
          </template>
        </div>
      </v-list-group>
    </template>
  </v-list>
</template>

<style scoped>
.border-l-2 {
  border-left: 2px solid rgba(255, 255, 255, 0.3);
}
.server-link:hover {
  text-decoration: underline !important;
  color: #2196f3; /* Primary Blue */
}
</style>
