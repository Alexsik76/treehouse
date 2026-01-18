import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ServerDetails from '@/views/ServerDetails.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/server/:id',
      name: 'server-details',
      component: ServerDetails,
      props: true
    }
  ]
})

export default router
