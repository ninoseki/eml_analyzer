import "@fortawesome/fontawesome-free/css/all.css";
import "@fortawesome/fontawesome-free/js/all.js";
import "@mdi/font/css/materialdesignicons.css";
import "buefy/dist/buefy.css";
import "highlight.js/styles/androidstudio.css";

import Buefy from "buefy";
import Vue from "vue";

import App from "@/App.vue";
import router from "@/router";
import { toCommaSeparatedString } from "@/utils/comma_separated";
import { secondsToHumanize } from "@/utils/seconds_to_humanize";

Vue.use(Buefy);

Vue.filter("toCommaSeparatedString", toCommaSeparatedString);
Vue.filter("secondsToHumanize", secondsToHumanize);

Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
