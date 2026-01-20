<script setup lang="ts">
import { ref } from "vue";
import {
  useInfrastructure,
  createInfrastructureItem,
  updateInfrastructureItem,
  deleteInfrastructureItem,
} from "@/services/api";
import type {
  InfrastructureItem,
  InfrastructureItemCreate,
} from "@/types/infrastructure";
import ServerCard from "@/components/ServerCard.vue";
import ItemDialog from "@/components/ItemDialog.vue";
import DeleteConfirmDialog from "@/components/DeleteConfirmDialog.vue";

// Use Composables for data fetching
const {
  isFetching: loading,
  error,
  data: items,
  execute: refreshInfrastructure,
} = useInfrastructure();

// Dialog State
const dialogOpen = ref(false);
const dialogError = ref<string | null>(null);
const selectedParent = ref<number | null>(null);
const selectedItemToEdit = ref<InfrastructureItem | null>(null);

// Delete Dialog State (retaining for future use, though deleting from card might need a button)
const deleteDialogOpen = ref(false);
const itemToDelete = ref<InfrastructureItem | null>(null);

const openAddDialog = (parentId?: number) => {
  selectedParent.value = parentId || null;
  selectedItemToEdit.value = null; // Reset edit mode
  dialogError.value = null;
  dialogOpen.value = true;
};

// Currently no edit button on card, but keeping handler
const openEditDialog = (item: InfrastructureItem) => {
  selectedItemToEdit.value = item;
  selectedParent.value = item.parent_id || null;
  dialogOpen.value = true;
};

const handleSaveItem = async (item: InfrastructureItemCreate) => {
  dialogError.value = null;
  try {
    if (selectedItemToEdit.value) {
      await updateInfrastructureItem(selectedItemToEdit.value.id, item);
    } else {
      await createInfrastructureItem(item);
    }
    dialogOpen.value = false;
    selectedItemToEdit.value = null;
    await refreshInfrastructure();
  } catch (e: any) {
    console.error(e);
    dialogError.value = e.message || "Failed to save item.";
  }
};

const handleConfirmDelete = async () => {
  if (!itemToDelete.value) return;
  try {
    await deleteInfrastructureItem(itemToDelete.value.id);
    deleteDialogOpen.value = false;
    itemToDelete.value = null;
    await refreshInfrastructure();
  } catch (e) {
    alert("Failed to delete item: " + e);
  }
};
</script>

<template>
  <v-container fluid class="fill-height align-start pa-6">
    <div class="w-100">
      <div class="d-flex justify-space-between align-center mb-6">
        <div>
          <h1 class="text-h4 font-weight-bold">Infrastructure</h1>
          <p class="text-medium-emphasis">Root Servers Overview</p>
        </div>
        <v-btn color="primary" prepend-icon="mdi-plus" @click="openAddDialog()">
          Add Server
        </v-btn>
      </div>

      <div v-if="loading" class="d-flex justify-center pa-12">
        <v-progress-circular
          indeterminate
          color="primary"
          size="64"
        ></v-progress-circular>
      </div>

      <v-alert v-else-if="error" type="error" variant="tonal" class="mb-4">
        {{ error }}
        <v-btn variant="text" size="small" @click="refreshInfrastructure()"
          >Retry</v-btn
        >
      </v-alert>

      <div
        v-else-if="!items || items.length === 0"
        class="text-center pa-12 text-medium-emphasis"
      >
        <v-icon icon="mdi-server-network-off" size="64" class="mb-4"></v-icon>
        <div class="text-h6">No infrastructure found</div>
        <v-btn
          variant="text"
          color="primary"
          class="mt-2"
          @click="openAddDialog()"
          >Create First Server</v-btn
        >
      </div>

      <v-row v-else>
        <!-- Filter for root items just in case, or assume useInfrastructure (API) returns tree roots -->
        <v-col v-for="server in items" :key="server.id" cols="12" md="6" lg="4">
          <ServerCard
            :server="server"
            class="cursor-pointer"
            @edit="openEditDialog"
          />
          <!-- Grid item for server card -->
        </v-col>
      </v-row>
    </div>

    <!-- Management Dialog -->
    <ItemDialog
      v-model="dialogOpen"
      :parent-id="selectedParent"
      :item-to-edit="selectedItemToEdit"
      :error-message="dialogError"
      @update:error-message="dialogError = $event"
      @save="handleSaveItem"
    />

    <!-- Delete Confirmation Dialog -->
    <DeleteConfirmDialog
      v-model="deleteDialogOpen"
      :item="itemToDelete"
      @confirm="handleConfirmDelete"
    />
  </v-container>
</template>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}
</style>
