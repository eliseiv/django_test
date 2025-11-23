<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { loadStripe } from '@stripe/stripe-js'

const route = useRoute()
const loading = ref(true)
const error = ref(null)
const order = ref(null)

const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLIC_KEY)

onMounted(async () => {
  try {
    const response = await axios.get(`/api/order/${route.params.id}/`)
    order.value = response.data
  } catch (e) {
    error.value = "Failed to load order"
    console.error(e)
  } finally {
    loading.value = false
  }
})

const total = computed(() => {
    if (!order.value) return 0;
    let sum = order.value.items.reduce((acc, item) => acc + item.price, 0);
    
    // Note: Accurate calculation including tax/discount should match backend logic.
    // This is just for display estimation.
    // Real checkout happens on Stripe side which uses backend logic.
    return sum;
})

const currency = computed(() => {
    if (order.value && order.value.items.length > 0) {
        return order.value.items[0].currency.toUpperCase();
    }
    return '';
})

const handleBuyOrder = async () => {
  try {
    const response = await axios.get(`/api/buy_order/${route.params.id}/`)
    const session = response.data
    const stripe = await stripePromise
    
    const { error } = await stripe.redirectToCheckout({
      sessionId: session.id,
    })
    
    if (error) {
      console.error(error)
      alert(error.message)
    }
  } catch (e) {
    console.error("Buy failed", e)
    const msg = e.response?.data?.error || e.message;
    alert("Buy failed: " + msg)
  }
}
</script>

<template>
  <div class="container">
    <div v-if="loading">Loading Order...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <div v-else-if="order">
        <h1>Order #{{ order.id }}</h1>
        
        <div class="order-items">
            <div v-for="item in order.items" :key="item.id" class="order-item">
                <span>{{ item.name }}</span>
                <span class="price">{{ (item.price / 100).toFixed(2) }} {{ item.currency.toUpperCase() }}</span>
            </div>
        </div>
        
        <div class="summary">
            <p><strong>Items count:</strong> {{ order.items.length }}</p>
            <p v-if="order.discount"><strong>Discount:</strong> {{ order.discount }}% (Applied at checkout)</p>
            <p v-if="order.tax"><strong>Tax:</strong> {{ order.tax }}% (Applied at checkout)</p>
            <hr>
            <p class="total">Total Base: {{ (total / 100).toFixed(2) }} {{ currency }}</p>
            <small>Final price with tax/discount calculated on payment page</small>
        </div>

        <button @click="handleBuyOrder" class="pay-btn">Pay for Order</button>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  background: #f9f9f9;
  border-radius: 8px;
  margin-top: 2rem;
}
.order-items {
    margin: 20px 0;
    border-top: 1px solid #eee;
}
.order-item {
    display: flex;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid #eee;
}
.price {
    font-weight: bold;
}
.summary {
    text-align: right;
    margin-top: 20px;
}
.total {
    font-size: 1.2em;
    font-weight: bold;
    color: #5469d4;
}
.pay-btn {
  background-color: #5469d4;
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 18px;
  width: 100%;
  margin-top: 20px;
}
.pay-btn:hover {
  background-color: #4455a9;
}
.error {
    color: red;
    text-align: center;
}
</style>
