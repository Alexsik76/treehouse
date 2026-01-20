<script setup lang="ts">
import { computed, ref } from "vue";
import type { InfrastructureItem } from "@/types/infrastructure";

import { useRouter } from "vue-router";
import { getOsIcon } from "@/utils/icons";

const props = defineProps<{
  server: InfrastructureItem;
}>();

const emit = defineEmits<{
  (e: "edit", item: InfrastructureItem): void;
}>();

const router = useRouter();
const isFlipped = ref(false);

const toggleFlip = () => {
  isFlipped.value = !isFlipped.value;
};

const handleEditClick = (event: Event) => {
  event.stopPropagation(); // Prevent flip
  emit("edit", props.server);
};

const navigateToDetail = (type: "vm" | "container") => {
  router.push({
    name: "server-details",
    params: { id: props.server.id },
    query: { type },
  });
};

// Helper to count immediate children by type (non-recursive)
const countByType = (items: InfrastructureItem[], type: string): number => {
  return items.filter((item) => item.type === type).length;
};

const vmCount = computed(() => countByType(props.server.children || [], "vm"));
const containerCount = computed(() =>
  countByType(props.server.children || [], "container"),
);

const status = computed(() => {
  const s = props.server.specs?.status;
  if (s === "online") return "online";
  if (s === "offline") return "offline";
  return "unknown";
});

const statusColor = computed(() => {
  switch (status.value) {
    case "online":
      return "success";
    case "offline":
      return "error";
    default:
      return "grey-lighten-1";
  }
});

const osIcon = computed(() => {
  return getOsIcon(props.server.specs?.os);
});

const lastUpdate = computed(() => {
  return new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
});
</script>

<template>
  <div class="flip-card" :class="{ flipped: isFlipped }" @click="toggleFlip">
    <div class="flip-card-inner">
      <!-- Front Side -->
      <div class="flip-card-front">
        <v-card class="fill-height acrylic-card">
          <div class="card-bg-icon">
            <v-icon :icon="osIcon" size="150" color="bg-icon-color"></v-icon>
          </div>

          <v-card-item>
            <template v-slot:prepend>
              <v-avatar color="surface-variant" size="x-large">
                <v-icon :icon="osIcon" size="32"></v-icon>
              </v-avatar>
            </template>
            <template v-slot:append>
              <v-btn
                icon="mdi-pencil"
                variant="text"
                density="compact"
                color="secondary"
                @click="handleEditClick"
              ></v-btn>
            </template>

            <v-card-title class="text-h6 font-weight-bold">
              {{ server.name }}
            </v-card-title>
            <v-card-subtitle>
              <div class="d-flex align-center">
                <v-icon
                  icon="mdi-circle-medium"
                  :color="statusColor"
                  class="mr-1"
                ></v-icon>
                <span class="text-caption text-uppercase">{{ status }}</span>
              </div>
            </v-card-subtitle>
          </v-card-item>

          <v-card-text class="pt-2 position-relative">
            <div class="d-flex flex-column gap-1">
              <div class="d-flex align-center text-body-2">
                <v-icon
                  icon="mdi-ip"
                  size="small"
                  class="mr-2 opacity-60"
                ></v-icon>
                {{ server.ip_address || "No IP" }}
              </div>
              <div class="d-flex align-center text-body-2">
                <v-icon
                  icon="mdi-dns"
                  size="small"
                  class="mr-2 opacity-60"
                ></v-icon>
                {{ server.dns_name || "No DNS" }}
              </div>
            </div>

            <v-divider class="my-3 opacity-20"></v-divider>

            <div class="d-flex justify-space-around stats-row mt-4">
              <div
                class="text-center stat-item cursor-pointer pa-3 rounded-lg flex-grow-1 mr-2 elevation-1"
                @click.stop="navigateToDetail('vm')"
                v-ripple
              >
                <v-icon
                  icon="mdi-desktop-tower"
                  color="primary"
                  size="large"
                  class="mb-1"
                ></v-icon>
                <div class="text-h5 font-weight-bold">{{ vmCount }}</div>
                <div class="text-caption font-weight-medium">VMs</div>
              </div>
              <div
                class="text-center stat-item cursor-pointer pa-3 rounded-lg flex-grow-1 ml-2 elevation-1"
                @click.stop="navigateToDetail('container')"
                v-ripple
              >
                <v-icon
                  icon="mdi-docker"
                  color="blue-darken-1"
                  size="large"
                  class="mb-1"
                ></v-icon>
                <div class="text-h5 font-weight-bold">{{ containerCount }}</div>
                <div class="text-caption font-weight-medium">Containers</div>
              </div>
            </div>
          </v-card-text>

          <div class="updated-timestamp text-caption text-disabled pa-2">
            Checked: {{ lastUpdate }}
          </div>
        </v-card>
      </div>

      <!-- Back Side -->
      <div class="flip-card-back">
        <v-card class="fill-height acrylic-card pa-4 d-flex flex-column">
          <div class="d-flex justify-space-between align-center mb-2">
            <span class="text-h6 font-weight-bold">Details</span>
            <v-icon icon="mdi-information-outline" size="small"></v-icon>
          </div>
          <v-divider class="mb-3"></v-divider>

          <div class="text-body-2">
            <p class="mb-2"><strong>OS Kernel:</strong> Linux 6.8.0-1-pve</p>
            <p class="mb-2"><strong>Uptime:</strong> 14 days, 3 hours</p>
            <p class="mb-2"><strong>CPU Usage:</strong> 12% (Avg)</p>
            <p class="mb-2"><strong>Memory:</strong> 32GB / 64GB</p>
            <p class="mb-2"><strong>Disk:</strong> 1.2TB / 2TB (NVMe)</p>

            <v-divider class="my-3"></v-divider>
            <p class="text-caption text-medium-emphasis">
              This is placeholder text for detailed information that will be
              fetched from the backend in the future.
            </p>

            <div class="d-flex justify-end mt-auto">
              <v-btn
                variant="tonal"
                size="small"
                color="secondary"
                prepend-icon="mdi-pencil"
                @click="handleEditClick"
              >
                Edit
              </v-btn>
            </div>
          </div>
        </v-card>
      </div>
    </div>
  </div>
</template>

<style scoped>
.flip-card {
  perspective: 1000px;
  height: 280px; /* Fixed height for card */
  cursor: pointer;
}

.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  text-align: left;
  transition: transform 0.6s;
  transform-style: preserve-3d;
}

.flip-card.flipped .flip-card-inner {
  transform: rotateX(180deg); /* Vertical flip */
}

.flip-card-front,
.flip-card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
  border-radius: 4px; /* Match v-card radius */
}

/* Front style */
.flip-card-front {
  z-index: 2;
  transform: rotateX(0deg);
}

/* Back style */
.flip-card-back {
  transform: rotateX(180deg);
  z-index: 1;
}

.acrylic-card {
  background: rgba(var(--v-theme-surface), 0.8) !important;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.card-bg-icon {
  position: absolute;
  right: -20px;
  bottom: -20px;
  opacity: 0.05;
  pointer-events: none;
  z-index: 0;
  transform: rotate(-15deg);
}

.updated-timestamp {
  position: absolute;
  bottom: 0;
  right: 0;
}

.stat-item {
  transition: all 0.2s ease-in-out;
  background-color: rgba(var(--v-theme-surface-variant), 0.1);
  border: 1px solid transparent;
  flex-basis: 0; /* Ensures equal width regardless of content */
}

.stat-item:hover {
  transform: translateY(-2px);
  background-color: rgba(var(--v-theme-primary), 0.1);
  border-color: rgba(var(--v-theme-primary), 0.3);
}

.gap-1 {
  gap: 4px;
}
</style>
