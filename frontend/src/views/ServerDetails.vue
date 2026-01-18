<script setup lang="ts">
import { useRoute, useRouter } from "vue-router";
import { useInfrastructureItem } from "@/services/api";
import ServerSpecs from "@/components/ServerSpecs.vue";
import ServerNetworkInfo from "@/components/ServerNetworkInfo.vue";

const route = useRoute();
const router = useRouter();

const id = Number(route.params.id);
const { data: item, isFetching: loading, error } = useInfrastructureItem(id);
</script>

<template>
  <v-container>
    <v-btn
      variant="text"
      icon="mdi-arrow-left"
      @click="router.back()"
      class="mb-4"
    ></v-btn>

    <div v-if="loading" class="d-flex justify-center">
      <v-progress-circular indeterminate></v-progress-circular>
    </div>

    <div v-else-if="error">
      <v-alert type="error">{{ error }}</v-alert>
    </div>

    <v-card v-else-if="item" class="mx-auto" max-width="800">
      <v-card-item>
        <template v-slot:prepend>
          <v-icon size="x-large" color="primary">mdi-server-network</v-icon>
        </template>
        <v-card-title class="text-h4">
          {{ item.name }}
        </v-card-title>
        <v-card-subtitle class="text-h6 text-high-emphasis opacity-70">
          {{ item.type }}
        </v-card-subtitle>
      </v-card-item>

      <v-divider></v-divider>

      <v-card-text class="pa-6">
        <ServerNetworkInfo
          :ip-address="item.ip_address"
          :dns-name="item.dns_name"
        />

        <v-divider class="my-4"></v-divider>

        <ServerSpecs :specs="item.specs" />
      </v-card-text>
    </v-card>
  </v-container>
</template>
