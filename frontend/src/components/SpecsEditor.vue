<script setup lang="ts">
import { ref, computed } from "vue";
import { InfrastructureType } from "@/types/infrastructure";

const props = defineProps<{
  modelValue: Record<string, string>;
  type: InfrastructureType;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: Record<string, string>): void;
}>();

// 1. Preset Keys: Підказки залежно від типу
const PRESET_KEYS: Record<InfrastructureType, string[]> = {
  [InfrastructureType.SERVER]: ["os", "cpu", "ram", "disk"],
  [InfrastructureType.VM]: ["os", "vCpu", "memory", "hypervisor"],
  [InfrastructureType.CONTAINER]: [
    "image",
    "ports",
    "volumes",
    "restart_policy",
  ],
  [InfrastructureType.SWITCH]: ["ports_count", "firmware", "vlan"],
  [InfrastructureType.ROUTER]: ["firmware", "vpn_proto"],
  [InfrastructureType.OTHER]: ["description", "location"],
};

// Auto-suggest keys based on selected Type
const availableKeys = computed(() => PRESET_KEYS[props.type] || []);

const newKey = ref("");
const newValue = ref("");

// Helper to update parent v-model
const updateSpecs = (newSpecs: Record<string, string>) => {
  emit("update:modelValue", newSpecs);
};

const addSpec = () => {
  if (newKey.value && newValue.value) {
    updateSpecs({ ...props.modelValue, [newKey.value]: newValue.value });
    newKey.value = "";
    newValue.value = "";
  }
};

const removeSpec = (key: string) => {
  const copy = { ...props.modelValue };
  delete copy[key];
  updateSpecs(copy);
};

// Auto-fill Key when clicking a chip
const usePreset = (key: string) => {
  newKey.value = key;
};
</script>

<template>
  <div class="specs-editor">
    <div class="text-subtitle-2 mb-2">Specifications</div>

    <v-sheet
      border
      rounded
      class="pa-2 mb-3"
      v-if="Object.keys(modelValue).length > 0"
    >
      <div
        v-for="(val, key) in modelValue"
        :key="key"
        class="d-flex align-center mb-1"
      >
        <v-btn
          icon="mdi-close"
          variant="text"
          color="error"
          size="x-small"
          class="mr-2"
          @click="removeSpec(key.toString())"
        ></v-btn>
        <span class="text-body-2 font-weight-bold mr-2">{{ key }}:</span>
        <span class="text-body-2 text-medium-emphasis">{{ val }}</span>
      </div>
    </v-sheet>
    <div v-else class="text-caption text-medium-emphasis mb-3">
      No specs added.
    </div>

    <div class="mb-2">
      <v-chip
        v-for="key in availableKeys"
        :key="key"
        size="x-small"
        class="mr-1 mb-1"
        :color="modelValue[key] ? 'grey' : 'primary'"
        variant="tonal"
        @click="usePreset(key)"
        :disabled="!!modelValue[key]"
      >
        {{ key }}
      </v-chip>
    </div>

    <div class="d-flex align-center">
      <v-text-field
        v-model="newKey"
        label="Key"
        density="compact"
        hide-details
        variant="outlined"
        class="mr-2"
        placeholder="e.g. os"
      ></v-text-field>
      <v-text-field
        v-model="newValue"
        label="Value"
        density="compact"
        hide-details
        variant="outlined"
        class="mr-2"
        placeholder="e.g. Debian 12"
        @keyup.enter="addSpec"
      ></v-text-field>
      <v-btn
        icon="mdi-plus"
        size="small"
        color="primary"
        variant="tonal"
        @click="addSpec"
        :disabled="!newKey || !newValue"
      ></v-btn>
    </div>
  </div>
</template>
