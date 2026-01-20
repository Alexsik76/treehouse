import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import TreeView from '@/views/TreeView.vue'
import AboutView from '@/views/AboutView.vue'
import SettingsView from '@/views/SettingsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/tree',
      name: 'tree',
      component: TreeView
    },
    {
      path: "/server/:id",
      name: "server-details",
      component: () => import("../views/ServerDetailView.vue"),
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView
    },
    {
      path: '/settings',
      name: 'settings',
      component: SettingsView
    },
  ]
})

export default router
