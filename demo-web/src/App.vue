<template>
  <div id="app">
    <!-- 头部 -->
    <Header></Header>
    <!-- 侧边导航栏 -->
    <SideNavBar></SideNavBar>
    <SearchModle></SearchModle>
    <!-- 通知框 -->
    <Notice></Notice>

    <!-- 内容 -->
    <transition name="moveCartoon" appear>
      <div v-if="validate()" style="min-height: calc(100vh - 167px);">
        <router-view :key="$route.fullPath" />
      </div>
      <div v-else style="min-height:100vh">
        <router-view :key="$route.fullPath" />
      </div>
      <!-- <router-view :key="$route.fullPath" :style="!$store.state.noticeFlag ? 'margin-top: 80px;' : ''" /> -->
    </transition>
    <!-- 底部 -->
    <Footer></Footer>

    <!-- 登录模态框 -->
    <Login></Login>
    <!-- 微信登录模态框 -->
    <WechatLogin></WechatLogin>
    <!-- 忘记密码模态框 -->
    <ForgetModel></ForgetModel>
    <!-- 注册模态框 -->
    <RegisterModel></RegisterModel>
    <!-- 友链模态框 -->
    <LinkModel></LinkModel>
    <!-- 侧边栏 -->
    <Sidebar v-if="!isMobile"></Sidebar>
  </div>
</template>

<script>
import Header from '@/components/layout/Header.vue'
import SideNavBar from "@/components/layout/SideNavBar.vue";
import SearchModle from "@/components/layout/Search.vue";
import Home from '@/view/home/index.vue'
import Footer from '@/components/layout/Footer.vue'
import Sidebar from '@/components/layout/Sidebar.vue'
import Login from '@/components/model/Login.vue'
import ForgetModel from '@/components/model/ForgetModel.vue'
import RegisterModel from '@/components/model/RegisterModel.vue'
import LinkModel from '@/components/model/LinkModel.vue'
import WechatLogin from '@/components/model/WechatLogin.vue'
import Notice from '@/components/notice/Notice.vue'
import { getWebSiteInfo } from '@/api'
import { setSkin, getSkin } from '@/utils/auth'
export default {
  name: 'App',
  components: {
    Header,
    Footer,
    Sidebar,
    Home,
    Login,
    ForgetModel,
    RegisterModel,
    LinkModel,
    SideNavBar,
    Notice,
    WechatLogin,
    SearchModle
  },
  data() {
    return {
      widthPre: '',
      height: "min-height"
    }
  },
  methods: {
    validate() {
      return this.$route.path == '/search' || this.$route.path == '/category';
    }
  },

  created() {
    getWebSiteInfo().then(res => {
      let siteCount = {
        articleCount: res.extra.articleCount,
        tagCount: res.extra.tagCount,
        categoryCount: res.extra.categoryCount,
      }
      this.$store.commit("setWebSiteInfo", res.extra.webConfig)
      this.$store.commit("setSiteCount", siteCount)
      this.$store.commit("setTagCloud", res.extra.tagCloud)
      this.$store.commit("setHotArticles", res.extra.hotArticles)
      this.$store.commit("setNewArticleList", res.extra.newArticleList)
    })


  },
  beforeCreate() {
    if (getSkin() == null) {
      setSkin("shallow")
    } else {
      setSkin(getSkin())
    }
  },
  computed: {
    // 判断是否是手机端，如果是，返回true
    isMobile() {
      const flag = navigator.userAgent.match(
        /(phone|pad|pod|iPhone|iPod|ios|iPad|Android|Mobile|BlackBerry|IEMobile|MQQBrowser|JUC|Fennec|wOSBrowser|BrowserNG|WebOS|Symbian|Windows Phone)/i
      );
      return flag;
    },
  },
  mounted() {
    this.$setSkin()
  },

}
</script>

<style lang="scss" scoped>
/* 类名要对应回 name 的属性值 */
.moveCartoon-enter-active {
  animation: move 1s;
}

.moveCartoon-leave-active {
  animation: move 1s reverse;
}

@keyframes move {
  from {
    transform: translateX(-100%);
  }

  to {
    transform: translate(0);
  }
}

body {
  padding: 0;
  margin: 0;
}

#app {
  background: var(--body-color);
}

// ::-webkit-scrollbar {
//   width: 8px;
// }

// ::-webkit-scrollbar-thumb {
//   background: linear-gradient(180deg, #F0BBC3, #10A44A);
//   border-radius: 8px;
// }
</style>
