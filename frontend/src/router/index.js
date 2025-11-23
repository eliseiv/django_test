import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ItemView from '../views/ItemView.vue'
import OrderView from '../views/OrderView.vue'
import SuccessView from '../views/SuccessView.vue'
import CancelView from '../views/CancelView.vue'
import PaymentIntentView from '../views/PaymentIntentView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/item/:id',
      name: 'item',
      component: ItemView
    },
    {
      path: '/pay/:id', // New route for Payment Intent flow
      name: 'pay-intent',
      component: PaymentIntentView
    },
    {
      path: '/order/:id',
      name: 'order',
      component: OrderView
    },
    {
      path: '/success',
      name: 'success',
      component: SuccessView
    },
    {
      path: '/cancel',
      name: 'cancel',
      component: CancelView
    }
  ]
})

export default router
