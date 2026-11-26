import { createRouter, createWebHistory } from 'vue-router'
import { useAuth } from '../stores/auth'
import Home from '../views/HomeView.vue'

const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/kona-ba', name: 'about', component: () => import('../views/AboutView.vue') },
  { path: '/istoria', name: 'history', component: () => import('../views/HistoryView.vue') },
  { path: '/istoria/figura/:slug', name: 'figure', component: () => import('../views/FigureView.vue') },
  { path: '/lideransa', name: 'leadership', component: () => import('../views/LeadershipView.vue') },
  { path: '/atividade', name: 'activities', component: () => import('../views/ActivitiesView.vue') },
  { path: '/atividade/:slug', name: 'activity', component: () => import('../views/ActivityView.vue') },
  { path: '/notisia', name: 'news', component: () => import('../views/NewsView.vue') },
  { path: '/notisia/:slug', name: 'news-item', component: () => import('../views/NewsItemView.vue') },
  { path: '/galeria', name: 'gallery', component: () => import('../views/GalleryView.vue') },
  { path: '/dokumentu', name: 'documents', component: () => import('../views/DocumentsView.vue') },
  { path: '/estrutura', name: 'branches', component: () => import('../views/BranchesView.vue') },
  { path: '/kontaktu', name: 'contact', component: () => import('../views/ContactView.vue') },
  { path: '/sai-membru', name: 'join', component: () => import('../views/JoinView.vue'), meta: { guestOnly: true } },
  { path: '/tama', name: 'login', component: () => import('../views/LoginView.vue'), meta: { guestOnly: true } },
  { path: '/konta', name: 'dashboard', component: () => import('../views/DashboardView.vue'), meta: { auth: true } },
  { path: '/:pathMatch(.*)*', name: 'notfound', component: () => import('../views/NotFoundView.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, saved) {
    if (saved) return saved
    if (to.hash) return { el: to.hash }
    return { top: 0 }
  },
})

router.beforeEach(async (to) => {
  const auth = useAuth()
  if (!auth.ready) await auth.init()
  if (to.meta.auth && !auth.isLoggedIn) return { name: 'login', query: { next: to.fullPath } }
  if (to.meta.guestOnly && auth.isLoggedIn) return { name: 'dashboard' }
})

export default router
