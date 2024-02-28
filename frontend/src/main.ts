import 'bulma/css/bulma.css'
import 'bulma-helpers/css/bulma-helpers.min.css'
import 'font-awesome-animation/css/font-awesome-animation.min.css'

import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faAngleDown,
  faCopy,
  faDownload,
  faInfoCircle,
  faLink,
  faSearch,
  faSpinner,
  faUpload
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
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
  faCopy
)

import App from '@/App.vue'

const app = createApp(App)
app.component('font-awesome-icon', FontAwesomeIcon)
app.use(router).mount('#app')
