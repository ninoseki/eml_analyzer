import { createRouter, createWebHashHistory, type RouteRecordRaw } from 'vue-router'

import Cache from '@/views/Cache.vue'
import Home from '@/views/Home.vue'
import Lookup from '@/views/Lookup.vue'

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
