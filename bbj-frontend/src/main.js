import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

import axios from "axios";
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import { createMemoryHistory, createRouter } from 'vue-router'
import LoginPage from "./components/LoginPage.vue";
import MainPage from "./components/MainPage.vue";


const routes = [
    {path: '/', redirect: '/login'},
    {path:'/login', component: LoginPage},
    {path:'/index', component: MainPage},
]
const router = createRouter({
    history:createMemoryHistory(),
    routes,
})
import {ElMessage} from "element-plus";
import { Message } from '@element-plus/icons-vue'
import VueCookie from 'vue-cookies'






const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

axios.defaults.baseURL = 'http://localhost:8000';
app.use(VueCookie).use(router).mount('#app')
