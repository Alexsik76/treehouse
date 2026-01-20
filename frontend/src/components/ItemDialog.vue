<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { InfrastructureType } from "@/types/infrastructure";
import type { InfrastructureItemCreate } from "@/types/infrastructure";

const props = defineProps<{
  modelValue: boolean;
  parentId?: number | null;
  itemToEdit?: InfrastructureItemCreate | null;
  errorMessage?: string | null;
  defaultType?: InfrastructureType; // New prop
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void;
  (e: "save", item: InfrastructureItemCreate): void;
  (e: "update:errorMessage", value: string | null): void;
}>();

const dialog = computed({
  get: () => props.modelValue,
  set: (val) => emit("update:modelValue", val),
});

const isEditing = computed(() => !!props.itemToEdit);

const localItem = ref<InfrastructureItemCreate>({
  name: "",
  type: props.defaultType || InfrastructureType.SERVER,
  ip_address: "",
  dns_name: "",
  specs: {},
  parent_id: props.parentId || null,
});

// Specs management (Simple Key-Value pair for demo)
const specKey = ref("");
const specValue = ref("");

const addSpec = () => {
  if (specKey.value && specValue.value) {
    localItem.value.specs[specKey.value] = specValue.value;
    specKey.value = "";
    specValue.value = "";
  }
};

const removeSpec = (key: string) => {
  delete localItem.value.specs[key];
};

// Reset form when dialog opens
watch(dialog, (val) => {
  if (val) {
    if (props.itemToEdit) {
      // Edit Mode: Clone existing item
      localItem.value = {
        name: props.itemToEdit.name,
        type: props.itemToEdit.type,
        ip_address: props.itemToEdit.ip_address,
        dns_name: props.itemToEdit.dns_name,
        specs: { ...props.itemToEdit.specs }, // Shallow copy specs
        parent_id: props.itemToEdit.parent_id,
      };
    } else {
      // Create Mode: Reset to default
      localItem.value = {
        name: "",
        type: props.defaultType || InfrastructureType.SERVER,
        ip_address: "",
        dns_name: "",
        specs: {},
        parent_id: props.parentId || null,
      };
    }
    specKey.value = "";
    specValue.value = "";
  }
});

const error = ref<string | null>(null);

const save = async () => {
  if (!localItem.value.name) {
    error.value = "Name is required.";
    return;
  }
  error.value = null;
  localItem.value.parent_id = props.parentId || null;
  emit("save", { ...localItem.value });
};

const close = () => {
  dialog.value = false;
};
</script>

<template>
  <v-dialog v-model="dialog" max-width="500px">
    <v-card>
      <v-card-title>
        <span class="text-h5">{{
          isEditing ? "Edit Item" : "New Infrastructure Item"
        }}</span>
      </v-card-title>

      <v-card-text>
        <v-alert
          v-if="errorMessage || error"
          type="error"
          variant="tonal"
          class="mb-4"
          closable
          @click:close="emit('update:errorMessage', null)"
        >
          {{ errorMessage || error }}
        </v-alert>
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-model="localItem.name"
                label="Name"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-select
                v-model="localItem.type"
                :items="Object.values(InfrastructureType)"
                label="Type"
                required
              ></v-select>
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model="localItem.ip_address"
                label="IP Address"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model="localItem.dns_name"
                label="DNS Name"
                hint="e.g. server-01.local"
                persistent-hint
              ></v-text-field>
            </v-col>

            <!-- Dynamic Specs -->
            <v-col cols="12">
              <div class="text-subtitle-2 mb-2">Specs</div>
              <div
                v-for="(val, key) in localItem.specs"
                :key="key"
                class="d-flex align-center"
              >
                <v-icon
                  size="small"
                  color="error"
                  class="mr-2"
                  @click="removeSpec(key.toString())"
                  >mdi-delete</v-icon
                >
                <strong>{{ key }}:</strong> &nbsp; {{ val }}
              </div>

              <v-divider class="my-2"></v-divider>

              <div class="d-flex align-center mt-2">
                <v-text-field
                  v-model="specKey"
                  label="Key"
                  density="compact"
                  hide-details
                  class="mr-2"
                ></v-text-field>
                <v-text-field
                  v-model="specValue"
                  label="Value"
                  density="compact"
                  hide-details
                  class="mr-2"
                ></v-text-field>
                <v-btn
                  icon="mdi-plus"
                  size="small"
                  @click="addSpec"
                  color="primary"
                ></v-btn>
              </div>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue-darken-1" variant="text" @click="close"
          >Cancel</v-btn
        >
        <v-btn color="blue-darken-1" variant="text" @click="save">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
