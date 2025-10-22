import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import { setUser } from '@/utils/auth'
export default new Vuex.Store({
  state: {
    skin: 'shallow',//shallow浅色模式  //deep深色模式
    loginFlag: false,
    forgetFlag: false,
    registerFlag: false,
    wechatFlag: false,
    drawer: false,
    searchDrawer: false,
    linkFlag: false,
    userId: null,
    avatar: null,
    nickname: null,
    token: null,
    siteCount: {
      articleCount: 0,
      tagCount: 0,
      categoryCount: 0
    },
    webSiteInfo: {},
    noticeFlag: true,
    tagCloud: {},
    newArticleList: {},
    hotArticles: {},
  },
  mutations: {
    login(state, user) {
      setUser(JSON.stringify(user), 60 * 60)
      const bc = new BroadcastChannel('my-channel'); // 创建BroadcastChannel对象
      bc.postMessage({ userValue: JSON.stringify(user) }); // 发送通知
    },

    closeModel(state) {
      state.loginFlag = false;
      state.forgetFlag = false;
      state.registerFlag = false;
      state.wechatFlag = false;
      state.linkFlag = false;
    },
    setWebSiteInfo(state, newValue) {
      state.webSiteInfo = newValue
    },
    setTagCloud(state, newValue) {
      state.tagCloud = newValue
    },
    setNewArticleList(state, newValue) {
      state.newArticleList = newValue
    },
    setHotArticles(state, newValue) {
      state.hotArticles = newValue
    },
    setSkin(state, newValue) {
      state.skin = newValue
    },
    setNoticeFlag(state, newValue) {
      state.noticeFlag = newValue
    },
    setDrawer(state, newValue) {
      state.drawer = newValue
    },
    setSearchDrawer(state, newValue) {
      state.searchDrawer = newValue
    },
    setLinkFlag(state, newValue) {
      state.linkFlag = newValue
    },
    setLoginFlag(state, newValue) {
      state.loginFlag = newValue
    },
    setWechatFlag(state, newValue) {
      state.wechatFlag = newValue
    },
    setForgetFlag(state, newValue) {
      state.forgetFlag = newValue
    },
    setRegisterFlag(state, newValue) {
      state.registerFlag = newValue
    },
    setSiteCount(state, newValue) {
      state.siteCount = newValue
    },
    logout(state) {
      state.userId = null;
      state.avatar = null;
      state.nickname = null;
      state.token = null;
    },
  },

  // actions: {
  //   setSkin(context, value) {
  //     // 修改getskin的值
  //     context.commit('getskin', value)
  //   }
  // },
})