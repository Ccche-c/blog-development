<template>
    <div class="main-container">
        <div class="main">
            <div class="main-box">
                <Banner :images="bannerList" />
                <HotCategory :category-list="categoryList" />
                <ArticleList :article-list="articleList" />
            </div>
            <!-- 分页按钮 -->
            <pagination v-if="pageTotal > 0" :page="pageData.pageNo" :page-size="pageData.pageSize" :total="total"
                :on-page-change="onPage" class="pagi page-content" />
        </div>

        <Sidebar />
    </div>
</template>

<script>
import { fetchArticleList, featchHomeData } from '@/api'

import Banner from '@/components/banner/Banner.vue'
import HotCategory from '../category/HotCategory.vue'
import ArticleList from '../article/ArticleList.vue'
import Pagination from '@/components/pagination/index.vue'
import Sidebar from '@/components/sidebar/index.vue'
export default {
    components: {
        Banner,
        HotCategory,
        ArticleList,
        Pagination,
        Sidebar,
    },
    name: 'Home',
    data() {
        return {
            emojis: [],
            pageData: {
                pageNo: 1,
                pageSize: 6,
            },
            bannerList: [],
            categoryList: [],
            articleList: [],
            pageTotal: 0,
        };
    },
    computed: {
        total() {
            return this.pageTotal || 0;
        },
    },

    // require引用：
    mounted() {
        this.fetchArticleList()
        this.getHomeData()
    },
    methods: {
        // 分页
        onPage(pageNow) {
            this.pageData.pageNo = pageNow;
            document.documentElement.scrollTop = 400;
            new this.$wow.WOW().init()
            this.fetchArticleList()
        },
        fetchArticleList() {
            fetchArticleList(this.pageData).then(res => {
                this.articleList = res.data.records;
                this.pageTotal = res.data.total
            })
        },
        getHomeData() {
            featchHomeData().then(res => {
                this.categoryList = res.extra.categories
                this.bannerList = res.extra.articles
            })
        },
    },
}
</script>

<style lang="scss" scoped >
@media screen and (max-width: 1118px) {
    .main-container {
        display: flex;
        justify-content: center;

        .main {
            width: 100%;

            .main-box {
                border-radius: 10px;
            }
        }

    }
}

@media screen and (min-width: 1119px) {
    .main-container {
        display: flex;
        justify-content: center;


        .main {
            width: 55%;

            .main-box {
                border-radius: 10px;

                &:hover {
                    box-shadow: 5px 4px 8px 6px rgba(7, 17, 27, .06);
                    transition: all .3s;
                }
            }
        }

    }
}
</style>