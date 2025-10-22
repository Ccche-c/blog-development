<template>
    <div class="user-mian">
        <div class="content">
            <v-card class="warpper">
                <img class="avatarImg" :src="user.avatar" />
                <div class="">昵称：
                    <span class="nickname">
                        {{ user.nickname }}
                    </span>
                </div>
                <div class="intro">个人简介：{{ user.intro }}</div>
                <div class="intro">个人站点：<a :href="user.webSite">{{ user.webSite }}</a> </div>
            </v-card>
            <div class="btn-box">
                <Button @click="handleClike(0)" type="submit" class="btn">点赞的文章</Button>
                <Button @click="handleClike(1)" type="submit" class="btn">修改资料</Button>
            </div>
            <div class="empty-box" v-show="index == 0">
                <svg-icon icon-class="empty"></svg-icon>
                <div>
                    看来站点暂时还没有你喜欢的文章呢
                </div>
            </div>
            <div class="edit" v-show="index == 1">
                <!-- <div class="">个人头像：
                    <input type="file" accept=".png, .jpg" ref="file" @change="selectFile" />
                </div> -->
                <div class="">个人昵称： <input type="text" v-model="editUser.nickname" /> </div>
                <div class="">个人简介： <input type="text" v-model="editUser.intro" /></div>
                <div class="">个人站点： <input type="text" v-model="editUser.webSite" /> </div>
                <div class="">个人邮箱： <input type="text" v-model="editUser.email" /> </div>
                <div>
                    <v-btn @click="update" class="submit">提交</v-btn>
                </div>
            </div>
        </div>

    </div>
</template>
<script>
import { updateUserInfo, getUserInfo } from '@/api'
import { getUser } from '@/utils/auth'
export default {
    data() {
        return {
            user: {},
            editUser: {},
            index: 0,
            filename: '',

        }
    },
    created() {
        getUserInfo().then(res => {
            this.user = res.data
            this.editUser = JSON.parse(JSON.stringify(res.data))
        }).catch(err => {
            this.$router.go(-1);
        })
    },
    mounted() {
        let el = document.getElementsByClassName("btn")
        Array.prototype.forEach.call(el, function (element) {
            element.className = "btn"
        });
        el[this.index].className += " active"
    },
    methods: {
        // 选择文件
        selectFile(e) {
            console.log(this.$refs["file"].files);
            console.log(this.$refs["file"].files[0]);
            if (this.$refs["file"].files[0]) {
                this.filename = this.$refs["file"].files[0].name;
                this.selectFileobj = this.$refs["file"].files[0];
            } else {
                this.filename = "";
            }
        },
        handleClike(index) {
            let el = document.getElementsByClassName("btn")
            Array.prototype.forEach.call(el, function (element) {
                element.className = "btn"
            });
            el[index].className += " active"
            this.index = index
        },
        update() {
            updateUserInfo(this.editUser).then(res => {
                this.user = this.editUser
                this.user = JSON.parse(JSON.stringify(this.editUser))
                this.$toast({ type: "success", message: res.message });
            }).catch(err => {
                this.$toast({ type: "error", message: err.message });
            })
        }
    }
}
</script>
<style lang="scss" scoped>
@media screen and (max-width: 1118px) {
    .user-mian {
        display: flex;
        justify-content: center;
        position: relative;

        .content {
            width: 100%;
            height: 100%;
            margin-top: 80px;
            text-align: center;

            .warpper {
                background: url('https://picsum.photos/510/300?random');
                background-size: 100% 100%;
                background-repeat: no-repeat;
                width: 100%;
                height: 300px;
                color: #fff;

                .avatarImg {
                    width: 100px;
                    height: 100px;
                    margin-top: 50px;
                    line-height: 100px;
                    border-radius: 50% !important;
                    border: 1px solid #ccc;
                }

                .nickname {
                    font-weight: 700;
                    font-size: 20px;
                }

                .intro {
                    margin-top: 20px;

                    a {
                        text-decoration: none;
                        color: var(--theme-color);
                    }
                }

            }

            .btn-box {
                margin-top: 20px;
                margin-bottom: 15px;
                position: relative;

                &::after {
                    content: '';
                    position: absolute;
                    bottom: -10px;
                    left: 0;
                    border: 1px solid var(--border-line);
                    height: 1px;
                    width: 100%;

                }



                .btn {
                    margin-right: 40px;
                    color: var(--text-color);

                    &:last-child {
                        margin-left: 40px;
                    }
                }

                .active {
                    color: #00a7eb;
                }

            }

            .empty-box {
                margin-top: 30px;
                color: var(--text-color);
            }

            .edit {
                margin-top: 30px;


                div {
                    margin-bottom: 30px;
                    color: var(--text-color);

                    input {
                        border: 1px solid #ccc;
                        border-radius: 5px;
                        padding: 5px;
                        width: 250px;
                        color: var(--text-color);
                    }
                }

                .submit {
                    border: 1px solid #00a7eb;
                    width: 70px;
                    padding: 5px 0;
                    border-radius: 5px;
                    background-color: #00a7eb;
                }
            }
        }

    }
}

@media screen and (min-width: 1119px) {
    .user-mian {
        display: flex;
        justify-content: center;
        position: relative;

        .content {
            width: 60%;
            height: 100%;
            padding: 10px;
            margin-top: 80px;
            text-align: center;

            .warpper {
                background: url('https://picsum.photos/510/300?random');
                background-size: 100% 100%;
                background-repeat: no-repeat;
                width: 100%;
                height: 300px;
                color: #fff;

                .avatarImg {
                    width: 100px;
                    height: 100px;
                    margin-top: 50px;
                    line-height: 100px;
                    border-radius: 50% !important;
                    border: 1px solid #ccc;
                }

                .nickname {
                    font-weight: 700;
                    font-size: 20px;
                }

                .intro {
                    margin-top: 20px;

                    a {
                        text-decoration: none;
                        color: var(--theme-color);
                    }
                }

            }

            .btn-box {
                margin-top: 20px;
                margin-bottom: 15px;
                position: relative;
                color: var(--text-color);

                &::after {
                    content: '';
                    position: absolute;
                    bottom: -10px;
                    left: 0;
                    border: 1px solid var(--border-line);
                    height: 1px;
                    width: 100%;

                }

                .active {
                    color: #00a7eb;
                }

                .btn {
                    margin-right: 40px;

                    &:last-child {
                        margin-left: 40px;
                    }
                }
            }

            .empty-box {
                margin-top: 30px;
                color: var(--text-color);
            }

            .edit {
                margin-top: 30px;

                div {
                    margin-bottom: 30px;
                    color: var(--text-color);

                    input {
                        border: 1px solid #ccc;
                        border-radius: 5px;
                        padding: 5px;
                        width: 250px;
                        color: var(--text-color);
                    }
                }

                .submit {
                    border: 1px solid #00a7eb;
                    width: 70px;
                    padding: 5px 0;
                    border-radius: 5px;
                    background-color: #00a7eb;
                }
            }
        }

    }
}
</style>