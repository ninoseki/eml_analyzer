import { createRouter, createWebHashHistory, type RouteRecordRaw } from 'vue-router'

import Cache from '@/views/CacheView.vue'
import Home from '@/views/HomeView.vue'
import Lookup from '@/views/LookupView.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/lookup/:id',
    name: 'Lookup',
    component: Lookup,
    props: true
  },
  {
    path: '/cache',
    name: 'Cache',
    component: Cache
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
