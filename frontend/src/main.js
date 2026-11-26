import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { i18n } from './i18n'
import '@fontsource/alfa-slab-one/400.css'
import '@fontsource/alegreya-sans/400.css'
import '@fontsource/alegreya-sans/400-italic.css'
import '@fontsource/alegreya-sans/500.css'
import '@fontsource/alegreya-sans/700.css'
import './assets/main.css'

document.documentElement.lang = i18n.global.locale.value

createApp(App).use(createPinia()).use(router).use(i18n).mount('#app')
