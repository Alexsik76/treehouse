<script setup lang="ts">
defineProps<{
  ipAddress?: string | null;
  dnsName?: string | null;
}>();
</script>

<template>
  <v-row>
    <v-col cols="12" md="6">
      <v-list-item>
        <template v-slot:prepend>
          <v-icon color="info">mdi-ip-network</v-icon>
        </template>
        <v-list-item-title>IP Address</v-list-item-title>
        <v-list-item-subtitle class="text-body-1 text-high-emphasis">
          {{ ipAddress || "Not set" }}
        </v-list-item-subtitle>
      </v-list-item>
    </v-col>
    <v-col cols="12" md="6">
      <v-list-item>
        <template v-slot:prepend>
          <v-icon color="purple">mdi-domain</v-icon>
        </template>
        <v-list-item-title>DNS Name</v-list-item-title>
        <v-list-item-subtitle class="text-body-1 text-high-emphasis">
          {{ dnsName || "Not set" }}
        </v-list-item-subtitle>
      </v-list-item>
    </v-col>
  </v-row>
</template>
