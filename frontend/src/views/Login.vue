<template>

    <DHeader/>
        <div id="signin">
            <h3>登录账号</h3>
            <form>
                <div class="form-elem">
                    <span>账号：</span>
                    <input v-model="signinName" type="text" placeholder="输入用户名">
                </div>

                <div class="form-elem">
                    <span>密码：</span>
                    <input v-model="signinPwd" type="password" placeholder="输入密码">
                </div>

                <div class="form-elem">
                    <button v-on:click.prevent="signin">登录</button>
                </div>
                <div class="form-elem">
                    <button @click="jump">注册</button>
                </div>
            </form>
        </div>

    <DFooter/>

</template>

<script>
    import axios from 'axios';
    import DHeader from '@/components/DHeader.vue'
    import DFooter from '@/components/DFooter.vue'

    export default {
        name: 'Login',
        components: {DHeader, DFooter},
        data: function () {
            return {
                signinName: '',
                signinPwd: '',
            }
        },
        methods: {
            jump(){
                this.$router.push({path: '/register'})
            },
            signin() {
                const that = this;
                axios
                    .post('/api/token/', {
                        username: that.signinName,
                        password: that.signinPwd,
                    })
                    .then(function (response) {
                        const storage = localStorage;
                        // Date.parse(...) 返回1970年1月1日UTC以来的毫秒数
                        // Token 被设置为1分钟，因此这里加上60000毫秒
                        const expiredTime = Date.parse(response.headers.date) + 60000;
                        //   // 设置 localStorage
                        storage.setItem('access.myweb', response.data.access);
                        storage.setItem('refresh.myweb', response.data.refresh);
                        storage.setItem('expiredTime.myweb', expiredTime);
                        storage.setItem('username.myweb', that.signinName);
                        // 路由跳转
                        // 登录成功后回到博客首页
                        that.$router.push({name: 'Home'});
                    })
                    .catch(function (error) {
                        alert('登陆失败，请重新登录！');
                        // Handling Error here...
                        // https://github.com/axios/axios#handling-errors
                    });
            },
        }
    }

/*
export default {
    name:'Register',
    components:{DHeader,DFooter},
    data() {
        return {
        ruleForm: {
            name: '',
            code: '',
            pwd: '',
            cpwd: '',
            email: ''
        },
        rules: {
            name: [{
            required: true,
            type: 'string',
            message: '请输入用户名',
            trigger: 'blur'
            }],
            pwd: [{
            required: true,
            message: '创建密码',
            trigger: 'blur'
            }],
            cpwd: [{
            required: true,
            message: '确认密码',
            trigger: 'blur'
            }, {
            validator: (rule, value, callback) => {
                if (value === '') {
                callback(new Error('请再次输入密码'))
                } else if (value !== this.ruleForm.pwd) {
                callback(new Error('两次输入密码不一致'))
                } else {
                callback()
                }
            },
            trigger: 'blur'
            }]
        }
        }
  },
  methods: {
    // 模拟登录
    signup() {
        const that = this;

        this.$refs['ruleForm'].validate((valid) => {
            
            if (valid) {
                 axios
                    .post('/api/user/', {
                        username: this.signupName,
                        password: this.signupPwd,
                    })
                    .then(function (response) {
                        that.signupResponse = response.data;
                        alert('用户注册成功，快去登录吧！');
                        setTimeout(
                        this.$router.push('/login'), 2000
                        )
                    })
                    .catch(function (error) {
                        alert(error.message);
                    });
                
            }
        })
    }
  }
}
*/
</script>

<style scoped>
    #grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
    }
    #signin {
        text-align: center;
    }
    .form-elem {
        padding: 10px;
    }
    input {
        height: 25px;
        padding-left: 10px;
    }
    button {
        height: 35px;
        cursor: pointer;
        border: none;
        outline: none;
        background: gray;
        color: whitesmoke;
        border-radius: 5px;
        width: 60px;
    }
</style>