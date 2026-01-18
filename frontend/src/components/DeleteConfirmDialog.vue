<script setup lang="ts">
import { ref, computed, watch } from "vue";
import type { InfrastructureItem } from "@/types/infrastructure";

const props = defineProps<{
  modelValue: boolean;
  item: InfrastructureItem | null;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void;
  (e: "confirm"): void;
}>();

const dialog = computed({
  get: () => props.modelValue,
  set: (val) => emit("update:modelValue", val),
});

const hasChildren = computed(() => {
  return props.item?.children && props.item.children.length > 0;
});

const confirmationInput = ref("");
const isConfirmed = computed(() => {
  if (!hasChildren.value) return true;
  return confirmationInput.value === props.item?.name;
});

// Reset input when dialog opens
watch(dialog, (val) => {
  if (val) {
    confirmationInput.value = "";
  }
});
</script>

<template>
  <v-dialog v-model="dialog" max-width="500">
    <v-card v-if="item">
      <v-card-title class="headline text-error" v-if="hasChildren">
        <v-icon color="error" class="mr-2">mdi-alert-octagon</v-icon>
        Warning: Cascading Delete
      </v-card-title>
      <v-card-title v-else> Confirm Deletion </v-card-title>

      <v-card-text>
        <p class="mb-4">
          Are you sure you want to delete <strong>{{ item.name }}</strong
          >?
        </p>

        <v-alert
          v-if="hasChildren"
          type="error"
          variant="tonal"
          border="start"
          class="mb-4"
        >
          This item has <strong>{{ item.children.length }}</strong> child
          resource(s). Deleting it will also permanently delete all children.
        </v-alert>

        <div v-if="hasChildren">
          <p class="text-caption mb-2">
            To confirm, please type the name of the item:
            <strong>{{ item.name }}</strong>
          </p>
          <v-text-field
            v-model="confirmationInput"
            variant="outlined"
            density="compact"
            placeholder="Type item name to confirm"
            :rules="[(v) => v === item?.name || 'Name does not match']"
          ></v-text-field>
        </div>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="grey" variant="text" @click="dialog = false"
          >Cancel</v-btn
        >
        <v-btn
          color="error"
          variant="flat"
          @click="$emit('confirm')"
          :disabled="!isConfirmed"
        >
          Delete
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
