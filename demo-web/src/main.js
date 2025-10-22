import Vue from 'vue'
import App from './App.vue'
import config from "./assets/js/config";
import './assets/font/iconfont.css'
import './assets/font/iconfont.js'
import InfiniteLoading from "vue-infinite-loading";
import store from './store'
import animated from 'animate.css'
import 'wowjs/css/libs/animate.css'
import wow from 'wowjs'
import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';
import githubTheme from '@kangc/v-md-editor/lib/theme/github.js';
import '@kangc/v-md-editor/lib/theme/style/github.css';
import createLineNumbertPlugin from '@kangc/v-md-editor/lib/plugins/line-number/index';
import createCopyCodePlugin from '@kangc/v-md-editor/lib/plugins/copy-code/index';
import '@kangc/v-md-editor/lib/plugins/copy-code/copy-code.css';
import hljs from 'highlight.js';
import "../src/icons";
import Toast from "./components/toast/index";
import vuetify from '@/plugins/vuetify'
import { vueBaberrage } from 'vue-baberrage'
import { setSkin } from '@/utils/skin'
import jsCookie from 'js-cookie'
Vue.prototype.$cookie = jsCookie;  // 在页面里可直接用 this.$cookie 调用
Vue.prototype.$setSkin = setSkin;

Vue.use(vueBaberrage)
VMdPreview.use(githubTheme, {
  Hljs: hljs,
});
VMdPreview.use(createLineNumbertPlugin())
VMdPreview.use(createCopyCodePlugin())
Vue.use(VMdPreview);
Vue.use(Toast);
Vue.prototype.$wow = wow
Vue.use(InfiniteLoading);

Vue.config.productionTip = false
Vue.prototype.config = config;
import router from './router'

new Vue({
  store,
  router,
  vuetify,
  render: h => h(App),
}).$mount('#app')

router.beforeEach((to, from, next) => {
  // if (to.path) {
  //  window._hmt.push(['_trackPageview', to.fullPath]);
  //   }
  // }
  /* 路由发生变化修改页面title */
  if (to.meta.title) {
    document.title = to.meta.title
  }
  next()
})
router.afterEach(() => {
  window.scrollTo({
    top: 0,
    behavior: "instant"
  });
});


