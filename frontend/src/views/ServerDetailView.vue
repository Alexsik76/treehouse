<script setup lang="ts">
import { computed, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
  useInfrastructure,
  createInfrastructureItem,
  updateInfrastructureItem,
} from "@/services/api";
import type {
  InfrastructureItemCreate,
  InfrastructureItem,
} from "@/types/infrastructure";
import ServerCard from "@/components/ServerCard.vue";
import ItemDialog from "@/components/ItemDialog.vue";
import { getOsIcon } from "@/utils/icons";
import { findItemById } from "@/utils/tree";

const route = useRoute();
const router = useRouter();

const {
  data: items,
  isFetching,
  execute: refreshInfrastructure,
} = useInfrastructure();

const serverId = computed(() => Number(route.params.id));
const typeFilter = computed(() => route.query.type as "vm" | "container");

const server = computed(() => {
  if (!items.value) return null;
  return findItemById(items.value, serverId.value);
});

const filteredChildren = computed(() => {
  if (!server.value || !server.value.children) return [];
  if (!typeFilter.value) return server.value.children;
  return server.value.children.filter((c) => c.type === typeFilter.value);
});

const osIcon = computed(() => {
  return getOsIcon(server.value?.specs?.os);
});

const goRoot = () => {
  router.push({ name: "tree" });
};

const goUp = () => {
  if (server.value?.parent_id) {
    router.push({
      name: "server-details",
      params: { id: server.value.parent_id },
      query: { type: server.value.type }, // Preserve context: if we act on a VM, go back to VM list
    });
  } else {
    goRoot();
  }
};

// Dialog State
const dialogOpen = ref(false);
const dialogError = ref<string | null>(null);
const itemToEdit = ref<InfrastructureItemCreate | null>(null);

const openAddDialog = () => {
  itemToEdit.value = null; // Reset edit item for creation
  dialogError.value = null;
  dialogOpen.value = true;
};

const openEditDialog = (item: InfrastructureItem) => {
  // We need to cast or map InfrastructureItem (from card) to InfrastructureItemCreate (for dialog)
  // Assuming they are compatible enough for the dialog prop, or we construct it.
  // The Dialog expects InfrastructureItemCreate which usually doesn't have ID, but localItem handles it.
  // We'll pass it as 'any' or compatible object to itemToEdit.
  itemToEdit.value = { ...item } as unknown as InfrastructureItemCreate;
  // We need ID for updating, so we might need to store it separately or ensure interface compatibility.
  // Let's store the ID implicitly in the itemToEdit object if we cast it.
  (itemToEdit.value as any).id = item.id;

  dialogError.value = null;
  dialogOpen.value = true;
};

const handleSaveItem = async (item: InfrastructureItemCreate) => {
  dialogError.value = null;
  // Enforce the correct parent based on context if creating
  if (!itemToEdit.value && server.value) {
    item.parent_id = server.value.id;
  }
  // Auto-set type if filtering and creating
  if (!itemToEdit.value && typeFilter.value) {
    item.type = typeFilter.value;
  }

  try {
    if (itemToEdit.value) {
      // Update
      const id = (itemToEdit.value as any).id;
      await updateInfrastructureItem(id, item);
    } else {
      // Create
      await createInfrastructureItem(item);
    }

    dialogOpen.value = false;
    await refreshInfrastructure();
  } catch (e: any) {
    console.error(e);
    dialogError.value = e.message || "Failed to save item.";
  }
};
</script>

<template>
  <div class="server-detail-container fill-height">
    <div v-if="server" class="hero-banner elevation-4 position-relative">
      <div class="hero-bg-icon">
        <v-icon :icon="osIcon" size="300" color="bg-icon-color"></v-icon>
      </div>

      <v-container fluid class="fill-height align-end pb-6 px-8">
        <div
          class="d-flex align-end justify-space-between w-100 position-relative z-10"
        >
          <div class="d-flex align-end">
            <v-avatar
              color="surface-variant"
              size="80"
              class="mr-6 elevation-2"
            >
              <v-icon :icon="osIcon" size="40"></v-icon>
            </v-avatar>
            <div>
              <div class="text-h4 font-weight-bold text-white mb-2">
                {{ server.name }}
              </div>
              <div class="d-flex align-center gap-4">
                <v-chip
                  color="surface"
                  variant="flat"
                  size="small"
                  class="text-capitalize"
                >
                  {{
                    typeFilter === "vm"
                      ? "Virtual Machines"
                      : typeFilter
                        ? typeFilter + "s"
                        : "All Resources"
                  }}
                </v-chip>
                <div class="text-body-1 text-white opacity-80">
                  {{ server.ip_address }}
                </div>
              </div>
            </div>
          </div>

          <div class="d-flex align-center gap-4">
            <v-btn
              color="success"
              variant="flat"
              size="large"
              prepend-icon="mdi-plus"
              @click="openAddDialog"
            >
              Add
              {{
                typeFilter === "vm" ? "VM" : typeFilter ? typeFilter : "Item"
              }}
            </v-btn>

            <div class="d-flex gap-2">
              <v-btn
                v-if="server.parent_id"
                color="white"
                variant="tonal"
                size="large"
                prepend-icon="mdi-arrow-up"
                @click="goUp"
              >
                Up
              </v-btn>

              <v-btn
                color="white"
                variant="tonal"
                size="large"
                prepend-icon="mdi-home"
                @click="goRoot"
              >
                Root
              </v-btn>
            </div>
          </div>
        </div>
      </v-container>
    </div>

    <v-container v-if="server" class="mt-8" fluid>
      <div
        v-if="!filteredChildren.length"
        class="text-center pa-12 text-medium-emphasis"
      >
        <v-icon
          icon="mdi-package-variant-closed"
          size="64"
          class="mb-4"
        ></v-icon>
        <div class="text-h5">
          No
          {{
            typeFilter === "vm"
              ? "VMs"
              : typeFilter
                ? typeFilter + "s"
                : "items"
          }}
          found
        </div>
        <v-btn color="primary" class="mt-4" @click="openAddDialog">
          Create First {{ typeFilter === "vm" ? "VM" : typeFilter || "Item" }}
        </v-btn>
      </div>

      <v-row v-else>
        <v-col
          v-for="child in filteredChildren"
          :key="child.id"
          cols="12"
          md="6"
          lg="4"
        >
          <!-- Reuse ServerCard - it handles VMs/Containers too -->
          <ServerCard :server="child" @edit="openEditDialog" />
        </v-col>
      </v-row>
    </v-container>

    <div
      v-else-if="isFetching"
      class="d-flex justify-center align-center fill-height"
    >
      <v-progress-circular
        indeterminate
        color="primary"
        size="64"
      ></v-progress-circular>
    </div>

    <div
      v-else
      class="d-flex justify-center align-center fill-height flex-column"
    >
      <v-icon
        icon="mdi-alert-circle"
        size="64"
        color="error"
        class="mb-4"
      ></v-icon>
      <div class="text-h5">Server not found</div>
      <v-btn color="primary" class="mt-4" @click="goRoot">Return to Tree</v-btn>
    </div>

    <!-- Management Dialog -->
    <ItemDialog
      v-model="dialogOpen"
      :parent-id="server?.id"
      :item-to-edit="itemToEdit"
      :error-message="dialogError"
      :default-type="typeFilter"
      @update:error-message="dialogError = $event"
      @save="handleSaveItem"
    />
  </div>
</template>

<style scoped>
.server-detail-container {
  background-color: rgb(var(--v-theme-background));
}

.hero-banner {
  height: 200px;
  background: rgba(var(--v-theme-surface), 0.9);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
  /* Ensure the transition name is respected by view transitions */
  contain: paint;
}

.hero-bg-icon {
  position: absolute;
  right: -50px;
  top: -50px;
  opacity: 0.1;
  pointer-events: none;
  transform: rotate(15deg);
}

.z-10 {
  z-index: 10;
}

.gap-4 {
  gap: 16px;
}
</style>
