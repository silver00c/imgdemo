<template>

    <DHeader/>

    <div v-if="photo !== null" class="grid-container">
        <div>
            <!-- <h1 id="image">{{ photo.image }}</h1> -->
            
            <div class="image-container">
                <img 
                    :src="imageIfExists(photo)" 
                    alt="" 
                    class="image"
                />
            </div>
            <!-- 显示图片 -->

            <p id="subtitle">
                <div class="form-elem">
                    <!-- <a :download="imageIfExists(photo)"  :href="imageIfExists(photo)" >下载</a> -->
                    <button v-on:click.prevent="downloadPhoto()" style="background-color: mediumslateblue">下载</button>
                    &nbsp;&nbsp;&nbsp;
                    <button v-on:click.prevent="deletePhoto()" style="background-color: darkred">删除</button>
                </div>
                图片由 {{ photo.author.username }} 发布于 {{ formatted_time(photo.created) }}
            </p>
        </div>
    </div>

    <DFooter/>

</template>

<script>
    import DHeader from '@/components/DHeader.vue'
    import DFooter from '@/components/DFooter.vue'

    import axios from 'axios';
    import authorization from '@/utils/authorization';

    export default {
        name: 'PhotoDetail',
        components: {DHeader, DFooter},
        data: function () {
            return {
                photo: null,
                photoID:null,
            }
        },
        mounted() {
            axios
                .get('/api/photo/' + this.$route.params.id + '/')
                .then(response => (this.photo = response.data))
            const that = this;
            axios
                .get('/api/photo/' + that.$route.params.id + '/')
                .then(function (response) {
                    const data = response.data;
                    that.photo = data.photo;
                    that.photoID = data.id;
                })
        },
        methods: {
            formatted_time: function (iso_date_string) {
                const date = new Date(iso_date_string);
                return date.toLocaleDateString()
            },
            imageIfExists(photo) {
                if (photo) {
                    return photo.image
                }
            },
            // 文件下载
            download(photo) {
                // window.open(process.env.VUE_APP_BASE_API + "/hospital/file/downloadFile?tPath=" + tPath)
                var name = row.tFileName;
                var url = row.tFilePath;
                const a = document.createElement('a')
                a.setAttribute('download', name)
                a.setAttribute('target', '_blank')
                a.setAttribute('href', process.env.VUE_APP_BASE_API + "/hospital/file/downloadFile?tPath=" + url)
                a.click()
            },
            downloadPhoto(){
                console.log(this.photo)
                console.log("error here")
                var url = this.photo.image;
                const a = document.createElement('a')
                a.setAttribute('download', url)//"/media/photo/" +
                a.setAttribute('href', url)
                a.click()
            } ,
            deletePhoto() {
                const that = this;
                const token = localStorage.getItem('access.myweb');
                authorization()
                    .then((response) =>{
                        if (response[0]) {
                            axios
                                .delete('/api/photo/' + that.photoID + '/',
                                {
                                        headers: {Authorization: 'Bearer ' + token}
                                    })
                                .then(() => that.$router.push({name: 'Home'}))
                            }
                        else {
                            alert('令牌过期，请重新登录。')
                        }
                    })
            }
        }
    }

</script>

<style scoped>
    .grid-container {
        display: grid;
        grid-template-columns: 3fr 1fr;
    }


    /* #title {
        text-align: center;
        font-size: x-large;
    } */

    #subtitle {
        text-align: center;
        color: gray;
        font-size: small;
    }

    button {
        height: 35px;
        cursor: pointer;
        border: none;
        outline: none;
        background: steelblue;
        color: whitesmoke;
        border-radius: 5px;
        width: 60px;
    }
</style>