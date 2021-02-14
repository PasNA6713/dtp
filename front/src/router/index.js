import Vue from 'vue'
import VueRouter from 'vue-router'


Vue.use(VueRouter)

const routes = [
  {
    path: '/home',
    component: () => import('../components/pages/Home.vue'),
    name: 'home'
  },
  {
    path: '/signin',
    component: () => import('../components/pages/SignIn.vue'),
    name: 'signin'
  },
  {
    path: '/signup',
    component: () => import('../components/pages/SignUp.vue'),
    name: 'signup'
  },
  {
    path: '',
    name: 'main',
    component: () => import('../views/Main.vue'),
    children: [
      {
        path: 'statistics',
        component: () => import('../components/pages/Statistics.vue'),
        name: 'statistics'
      },
      {
        path: 'map',
        component: () => import('../components/pages/Map.vue'),
        name: 'map'
      },
      {
        path: 'about-project',
        component: () => import('../components/pages/AboutProject.vue'),
        name: 'about-project'
      }
    ]
  }
]


const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  linkActiveClass: "active",
  routes
})

export default router
