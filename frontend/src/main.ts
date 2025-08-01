import 'font-awesome-animation/css/font-awesome-animation.min.css'
import '@/style.css'

import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faAngleDown,
  faCopy,
  faDownload,
  faIdBadge,
  faInfoCircle,
  faLink,
  faSearch,
  faSpinner,
  faUpload
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { createPinia } from 'pinia'
import { createApp } from 'vue'

import router from '@/router'

library.add(
  faAngleDown,
  faLink,
  faSearch,
  faUpload,
  faSpinner,
  faDownload,
  faUpload,
  faInfoCircle,
  faCopy,
  faIdBadge
)
const pinia = createPinia()

import App from '@/App.vue'

const app = createApp(App)

app.component('font-awesome-icon', FontAwesomeIcon)
app.use(router)
app.use(pinia)

app.mount('#app')
