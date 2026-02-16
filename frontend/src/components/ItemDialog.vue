<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { InfrastructureType } from "@/types/infrastructure";
import type { InfrastructureItemCreate } from "@/types/infrastructure";
import SpecsEditor from "./SpecsEditor.vue"; // Import new component

const props = defineProps<{
  modelValue: boolean;
  parentId?: number | null;
  itemToEdit?: InfrastructureItemCreate | null;
  errorMessage?: string | null;
  defaultType?: InfrastructureType;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void;
  (e: "save", item: InfrastructureItemCreate): void;
  (e: "update:errorMessage", value: string | null): void;
}>();

// --- Local State ---
const localItem = ref<InfrastructureItemCreate>({
  name: "",
  type: InfrastructureType.SERVER, // Default, will be overwritten on open
  ip_address: "",
  dns_name: "",
  specs: {},
  parent_id: null,
});

const error = ref<string | null>(null);

// --- Computed ---
const dialog = computed({
  get: () => props.modelValue,
  set: (val) => emit("update:modelValue", val),
});

const isEditing = computed(() => !!props.itemToEdit);

// --- Logic ---

/**
 * Resets the form state explicitly. 
 * Called when dialog opens.
 */
const initForm = () => {
  error.value = null;
  emit("update:errorMessage", null);

  if (props.itemToEdit) {
    // Edit Mode: Deep clone to avoid mutating prop by reference issues
    // JSON parse/stringify is a cheap "lazy" deep clone for simple objects
    localItem.value = JSON.parse(JSON.stringify(props.itemToEdit));
  } else {
    // Create Mode
    localItem.value = {
      name: "",
      type: props.defaultType || InfrastructureType.SERVER,
      ip_address: "",
      dns_name: "",
      specs: {}, // SpecsEditor handles this object
      parent_id: props.parentId || null,
    };
  }
};

// Watch dialog open state to trigger init
watch(() => props.modelValue, (isOpen) => {
  if (isOpen) {
    initForm();
  }
});

const save = () => {
  if (!localItem.value.name) {
    error.value = "Name is required.";
    return;
  }
  // Clean empty strings for optional fields if needed
  if (!localItem.value.ip_address) localItem.value.ip_address = "";
  
  emit("save", localItem.value);
};

const close = () => {
  dialog.value = false;
};
</script>

<template>
  <v-dialog v-model="dialog" max-width="600px" persistent>
    <v-card>
      <v-card-title class="bg-primary text-white">
        <span class="text-h6">{{ isEditing ? "Edit Item" : "New Item" }}</span>
      </v-card-title>

      <v-card-text class="pt-4">
        <v-slide-y-transition>
          <v-alert
            v-if="errorMessage || error"
            type="error"
            variant="tonal"
            class="mb-4"
            closable
            density="compact"
            @click:close="error = null; emit('update:errorMessage', null)"
          >
            {{ errorMessage || error }}
          </v-alert>
        </v-slide-y-transition>

        <v-container class="pa-0">
          <v-row dense>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="localItem.name"
                label="Name"
                variant="outlined"
                density="compact"
                autofocus
                :rules="[v => !!v || 'Name is required']"
              ></v-text-field>
            </v-col>
            
            <v-col cols="12" md="6">
              <v-select
                v-model="localItem.type"
                :items="Object.values(InfrastructureType)"
                label="Type"
                variant="outlined"
                density="compact"
              ></v-select>
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                v-model="localItem.ip_address"
                label="IP Address"
                variant="outlined"
                density="compact"
                placeholder="192.168.1.1"
              ></v-text-field>
            </v-col>
            
            <v-col cols="12" md="6">
              <v-text-field
                v-model="localItem.dns_name"
                label="DNS Name"
                variant="outlined"
                density="compact"
                placeholder="srv.local"
              ></v-text-field>
            </v-col>

            <v-col cols="12">
              <v-divider class="my-3"></v-divider>
              <SpecsEditor 
                v-model="localItem.specs" 
                :type="localItem.type" 
              />
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>

      <v-card-actions class="pb-3 px-4">
        <v-spacer></v-spacer>
        <v-btn color="grey-darken-1" variant="text" @click="close">Cancel</v-btn>
        <v-btn color="primary" variant="elevated" @click="save" :disabled="!localItem.name">
          {{ isEditing ? 'Update' : 'Create' }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>