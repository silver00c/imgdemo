import {createWebHistory, createRouter} from "vue-router";
import Home from "@/views/Home.vue";
import PhotoDetail from "@/views/PhotoDetail.vue";
import Register from "@/views/Register.vue";
import Login from "@/views/Login.vue";
import UserCenter from "@/views/UserCenter.vue";
import PhotoUpload from "@/views/PhotoUpload.vue"
const routes = [
    {
        path: "/",
        name: "Home",
        component: Home,
    },
    {
        path: "/photo/:id",
        name: "PhotoDetail",
        component: PhotoDetail
    },
    {
        path: "/register",
        name: "Register",
        component: Register
    },
    {
        path: "/login",
        name: "Login",
        component: Login
    },
    {
        path: "/user/:username",
        name: "UserCenter",
        component: UserCenter
    },
    {
        path: "/photo/upload",
        name: "PhotoUpload",
        component: PhotoUpload
    },
];

const router = createRouter({
    history: createWebHistory(), //具体路由形式为HTML5模式，部署时需额外配置
    routes,
});

export default router;