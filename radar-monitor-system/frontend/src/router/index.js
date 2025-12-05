import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/login.vue'
import manage from "../views/manage.vue"
import data from "../views/data.vue";
import heart_pic from "../views/heart_pic.vue";
import login from "../views/login.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [

    {path: '/', redirect: '/login'},

    {
      path:'/manage',
      component: manage,
      children:[
        {
          path: 'data',
          name: 'data',
          meta: { title: 'data' },
          component: data,
        },
        {
          path: 'heart_pic',
          name: 'heart_pic',
          meta: { title: 'heart_pic' },
          component: heart_pic,
        },
      ]
    },
    {path:'/login', component: login}
  ],
})

export default router
