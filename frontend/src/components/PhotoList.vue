<template>
    <div v-for="photo in info.results" v-bind:key="photo.url" id="photos">
        
        <div>
            <span
                  v-for="tag in photo.tags" 
                  v-bind:key="tag" 
                  class="tag"
            >
                {{ tag }}
            </span>
        </div>
        <router-link
                :to="{ name: 'PhotoDetail', params: { id: photo.id}}"
                class="photo-name"
        >
            <div class="image-container">
                <img :src="imageIfExists(photo)" alt="" class="image">
            </div>
        </router-link>
        <div>
            {{ formatted_time(photo.created) }}
        </div>
    </div>

    <div id="paginator">
        <span v-if="is_page_exists('previous')">
            <router-link :to="{ name: 'Home', query: { page: get_page_param('previous') } }">
                Prev
            </router-link>
        </span>
        <span class="current-page">
            {{ get_page_param('current') }}
        </span>
        <span v-if="is_page_exists('next')">
            <router-link :to="{ name: 'Home', query: { page: get_page_param('next') } }">
                Next
            </router-link>
        </span>
    </div>

</template>

<script>
    import axios from 'axios';

    export default {
        name: 'PhotoList',
        data: function () {
            return {
                info: ''
            }
        },
        mounted() {
            this.get_photo_data() 
            /*axios
                .get('/api/photo')
                .then(response => (this.info = response.data))*/
        },
        methods: {
            imageIfExists(photo) {
                if (photo) {
                    return photo.image
                }
            },
            formatted_time: function (iso_date_string) {
                const date = new Date(iso_date_string);
                return date.toLocaleDateString()
            },
            // 判断页面是否存在
            is_page_exists(direction) {
                if (direction === 'next') {
                    return this.info.next !== null
                }
                return this.info.previous !== null
            },
            // 获取页码
            get_page_param: function (direction) {
                try {
                    let url_string;
                    switch (direction) {
                        case 'next':
                            url_string = this.info.next;
                            break;
                        case 'previous':
                            url_string = this.info.previous;
                            break;
                        default:
                            return this.$route.query.page
                    }

                    const url = new URL(url_string);
                    return url.searchParams.get('page')
                }
                catch (err) {
                    return
                }
            },
            // 获取文章列表数据
            get_photo_data: function () {
                let url = '/api/photo';
                const page = Number(this.$route.query.page);
                if (!isNaN(page) && (page !== 0)) {
                    url = url + '/?page=' + page;
                }

                axios
                    .get(url)
                    .then(response => (this.info = response.data))
                    .catch(error => {
                        this.$message.error(err.message)
                        console.log(error)
                    })
            },
        },
        watch: {
            // 监听路由是否有变化
            $route() {
                this.get_photo_data()
            }
        }
    }

</script>

<!-- "scoped" 使样式仅在当前组件生效 -->
<style scoped>
    .image {
        width: 180px;
        border-radius: 10px;
        box-shadow: darkslategrey 0 0 12px;
    }

    .image-container {
        width: 200px;
    }

    #photos {
        padding: 10px;
    }

    .photo-name {
        font-size: large;
        font-weight: bolder;
        color: black;
        text-decoration: none;
        padding: 5px 0 5px 0;
    }

    .tag {
        padding: 2px 5px 2px 5px;
        margin: 5px 5px 5px 0;
        font-family: Georgia, Arial, sans-serif;
        font-size: small;
        background-color: #4e4e4e;
        color: whitesmoke;
        border-radius: 5px;
    }

    #paginator {
        text-align: center;
        padding-top: 50px;
    }

    a {
        color: black;
    }

    .current-page {
        font-size: x-large;
        font-weight: bold;
        padding-left: 10px;
        padding-right: 10px;
    }
</style>