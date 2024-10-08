import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import axios from "axios";
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import {ElMessage} from "element-plus";
import { Message } from '@element-plus/icons-vue'
const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
app.mount('#app')
axios.defaults.baseURL = 'http://localhost:8000';