<template>

    <DHeader/>
        <div id="signup">
            <h3>注册账号</h3>
            <form>
                <div class="form-elem">
                    <span>账号：</span> 
                    <input v-model="signupName" type="text" placeholder="输入用户名">
                </div>
                <div class="form-elem">
                    <span>密码：</span> 
                    <input v-model="signupPwd" type="password" placeholder="输入密码">
                </div>
                <div class="form-elem">
                    <button v-on:click.prevent="signup">提交</button>
                </div>
            </form>
        </div>
        <!-- <el-form
            ref="ruleForm"
            :model="ruleForm"
            :rules="rules"
            label-width="100px"
            class="demo-ruleForm"
            autocomplete="off"
        >
            <div>
                <el-form-item label="用户名" prop="name">
                    <el-input v-model="ruleForm.name" />
                </el-form-item> 
                <el-form-item label="密码" prop="pwd">
                    <el-input v-model="ruleForm.pwd" type="password" />
                </el-form-item>
                <el-form-item label="确认密码" prop="cpwd">
                    <el-input v-model="ruleForm.cpwd" type="password" />
                </el-form-item>
                <el-button v-on:click.prevent="signup">注册</el-button>
            </div>
        </el-form> -->
    <DFooter/>

</template>

<script>
    import axios from 'axios';
    import DHeader from '@/components/DHeader.vue'
    import DFooter from '@/components/DFooter.vue'

    export default {
        name: 'Register',
        components: {DHeader, DFooter},
        data: function () {
            return {
                signupName: '',
                signupPwd: '',
                signupResponse: null,
            }
        },
        methods: {
            signup() {
                const that = this;
                axios
                    .post('/api/user/', {
                        username: this.signupName,
                        password: this.signupPwd,
                    })
                    .then(function (response) {
                        that.signupResponse = response.data;
                        alert('用户注册成功，快去登录吧！');
                        that.$router.push({name: 'Login'});
                    })
                    .catch(function (error) {
                        alert(error.message);
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
    #signup {
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