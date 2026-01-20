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
import InfrastructureTree from "@/components/InfrastructureTree.vue";
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

// Delete Dialog State
const deleteDialogOpen = ref(false);
const itemToDelete = ref<InfrastructureItem | null>(null);

const openAddDialog = (parentId?: number) => {
  selectedParent.value = parentId || null;
  selectedItemToEdit.value = null; // Reset edit mode
  dialogError.value = null;
  dialogOpen.value = true;
};

const openEditDialog = (item: InfrastructureItem) => {
  selectedItemToEdit.value = item;
  selectedParent.value = item.parent_id || null;
  dialogOpen.value = true;
};

const handleSaveItem = async (item: InfrastructureItemCreate) => {
  dialogError.value = null;
  try {
    if (selectedItemToEdit.value) {
      // Update existing item
      await updateInfrastructureItem(selectedItemToEdit.value.id, item);
    } else {
      // Create new item
      await createInfrastructureItem(item);
    }
    dialogOpen.value = false;
    selectedItemToEdit.value = null;
    await refreshInfrastructure(); // Refresh list
  } catch (e: any) {
    console.error(e);
    // Extract message if possible
    dialogError.value = e.message || "Failed to save item.";
  }
};

const openDeleteDialog = (item: InfrastructureItem) => {
  itemToDelete.value = item;
  deleteDialogOpen.value = true;
};

const handleConfirmDelete = async () => {
  if (!itemToDelete.value) return;

  try {
    await deleteInfrastructureItem(itemToDelete.value.id);
    deleteDialogOpen.value = false;
    itemToDelete.value = null;
    await refreshInfrastructure(); // Refresh list
  } catch (e) {
    alert("Failed to delete item: " + e);
  }
};
</script>

<template>
  <v-container class="fill-height align-start justify-center">
    <v-card width="800" variant="outlined" class="mt-4">
      <v-card-item>
        <v-card-title>Infrastructure Map</v-card-title>
        <v-card-subtitle>Live view from Backend</v-card-subtitle>
      </v-card-item>

      <v-card-text>
        <div v-if="loading" class="d-flex justify-center pa-4">
          <v-progress-circular
            indeterminate
            color="primary"
          ></v-progress-circular>
        </div>

        <v-alert v-else-if="error" type="error" variant="tonal" class="mb-4">
          {{ error }}
          <v-btn variant="text" size="small" @click="refreshInfrastructure()"
            >Retry</v-btn
          >
        </v-alert>

        <div
          v-else-if="items && items.length === 0"
          class="text-center pa-4 text-medium-emphasis"
        >
          No items found.
          <v-btn variant="text" color="primary" @click="openAddDialog()"
            >Create First Item</v-btn
          >
        </div>

        <InfrastructureTree
          v-else
          :items="items || []"
          @delete="openDeleteDialog"
          @edit="openEditDialog"
          @add-child="openAddDialog"
        />
      </v-card-text>

      <v-card-actions>
        <v-btn block variant="tonal" color="primary" @click="openAddDialog()"
          >Add Root Server</v-btn
        >
      </v-card-actions>
    </v-card>

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
