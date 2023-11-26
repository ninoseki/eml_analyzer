import "@fortawesome/fontawesome-free/css/all.css"
import "@fortawesome/fontawesome-free/js/all.js"
import "@mdi/font/css/materialdesignicons.css"
import "buefy/dist/buefy.css"
import "highlight.js/styles/androidstudio.css"

import Buefy from "buefy"
import Vue from "vue"

import App from "@/App.vue"

Vue.use(Buefy)

Vue.config.productionTip = false

new Vue({
  render: (h) => h(App)
}).$mount("#app")
