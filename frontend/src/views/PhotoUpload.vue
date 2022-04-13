<template>
  <DHeader/>
    <el-form :model="form" ref="form" label-width="100px">
        <div class="form-elem">
            <span>分类：</span>
            <span
                v-for="category in categories"
                :key="category.id"
                >
            <!--样式也可以通过 :style 绑定-->
            <button
                    class="category-btn"
                    :style="categoryStyle(category)"
                    @click.prevent="chooseCategory(category)"
                    >
                {{category.title}}
            </button>
            </span>
        </div>
        <div class="form-elem">
            <span>标签：</span>
            <input v-model="tags" type="text" placeholder="输入标签，用逗号分隔">
        </div>

        <el-form-item width="200" align="center" label="选择文件" prop="path">
          <input type="file" class="image" accept="image/*" @change="getFile($event)" ref="inputer">
        </el-form-item>
        <br><br><br>
        <el-form-item class="form-elem">
            <button v-on:click.prevent="onSubmit($event)">提交</button>
        </el-form-item>
    </el-form>
    <!-- <div id="photo-upload">
        <h3>上传图片</h3>
        <form id="image_form">
            <div class="form-elem">
                <span>分类：</span>
                <span
                    v-for="category in categories"
                    :key="category.id"
                    >
                <button
                        class="category-btn"
                        :style="categoryStyle(category)"
                        @click.prevent="chooseCategory(category)"
                        >
                    {{category.title}}
                </button>
                </span>
            </div>

            <div class="form-elem">
                <span>标签：</span>
                <input v-model="tags" type="text" placeholder="输入标签，用逗号分隔">
            </div>

            <div class="form-elem">
                <span>图片：</span>
                <input
                    v-on:change="onFileChange"
                    type="file"
                    id="file"
                >
            </div>

            <div class="form-elem">
                <button v-on:click.prevent="submit">提交</button>
            </div>

        </form>
    </div> -->
  <DFooter/>
</template>

<script>
    import DHeader from '@/components/DHeader.vue'
    import DFooter from '@/components/DFooter.vue'
    import axios from 'axios'
    import authorization from '@/utils/authorization'
    export default {
        name: 'PhotoUpload',
        components: {DHeader, DFooter},
        data: function () {
            return {
                // 图片
                image: '',
                // 数据库中所有的分类
                categories: [],
                // 选定的分类
                selectedCategory: null,
                // 标签
                tags: '',
                formData:new FormData(),
            }
        },
        mounted() {
            axios
                .get('/api/category/')
                .then(response => this.categories = response.data)
        },
        methods: {
            // 根据分类是否被选中，按钮的颜色发生变化
            categoryStyle(category) {
                if (this.selectedCategory !== null && category.id === this.selectedCategory.id) {
                    return {
                        backgroundColor: 'black',
                    }
                }
                return {
                    backgroundColor: 'lightgrey',
                    color: 'black',
                }
            },
            // 选取分类的方法
            chooseCategory(category) {
                // 如果点击已选取的分类，则将 selectedCategory 置空
                if (this.selectedCategory !== null && this.selectedCategory.id === category.id) {
                    this.selectedCategory = null
                }
                // 如果没选中当前分类，则选中它
                else {
                    this.selectedCategory = category;
                }
            },
            getFile(event) {
                //this.form.multipartFile = event.target.files[0];
                if(this.formData.get('image')){//重新选择图片
                    this.formData.delete('image');
                }
                this.formData.append("image", event.target.files[0]);
            },
            onSubmit(event) {
                const that = this;
                // 前面封装的验证函数又用上了
                authorization()
                    //that.$refs['form'][0].validate((valid) => {
                    .then(function (response) {
                        if (response[0]) {
                            //event.preventDefault();
                            that.formData.delete('category');//防止二次修改表单后重复添加
                            that.formData.delete('tags');//防止二次修改表单后重复添加

                            if (that.selectedCategory) {
                                that.formData.append("category_id", that.selectedCategory.id);
                            }
                            // data.tags = that.tags
                            //     // 用逗号分隔标签
                            //     .split(/[,，]/)
                            //     // 剔除标签首尾空格
                            //     .map(x => x.trim())
                            //     // 剔除长度为零的无效标签
                            //     .filter(x => x.charAt(0) !== '');
                            that.formData.append("tags", that.tags
                                // 用逗号分隔标签
                                .split(/[,，]/)
                                // 剔除标签首尾空格
                                .map(x => x.trim())
                                // 剔除长度为零的无效标签
                                .filter(x => x.charAt(0) !== '')
                            );

                            const token = localStorage.getItem('access.myweb');
                            axios({
                                method: 'post', 
                                url:'/api/photo/', 
                                data:that.formData,
                                headers: {'Authorization': 'Bearer ' + token,'Content-Type':'multipart/form-data'}
                            }).then(function (response) {
                                    that.$router.push({name: 'PhotoDetail', params: {id: response.data.id}});
                                })
                                // ({data})=>{
                                // if(data.code===0){
                                //     this.$message({
                                //         showClose: true,
                                //         message: "成功",
                                //         type: "success"
                                //     });
                                // }else{
                                //     this.$notify({
                                //         title: "失败",
                                //         message: "修改失败",
                                //         type: "danger",
                                //         duration: 2000
                                //     });
                                //}
                            //})
                            .catch(function (error) {
                                console.log(error);
                            });
                        } else {
                            // console.log('error submit!!');
                            // return false;
                            alert('令牌过期，重新登录')
                        }
                    });
            },
        }
    }
</script>

<style scoped>
  .category-btn {
    margin-right: 10px;
  }
  #article-create {
    text-align: center;
    font-size: large;
  }
  form {
    text-align: left;
    padding-left: 100px;
    padding-right: 10px;
  }
  .form-elem {
    padding: 10px;
  }
  input {
    height: 25px;
    padding-left: 10px;
    width: 50%;
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