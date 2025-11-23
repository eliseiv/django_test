<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { loadStripe } from '@stripe/stripe-js'

const route = useRoute()
const item = ref(null)
const loading = ref(true)
const error = ref(null)

const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLIC_KEY || 'pk_test_placeholder')

onMounted(async () => {
  try {
    const response = await axios.get(`/api/item/${route.params.id}/`)
    item.value = response.data
  } catch (e) {
    error.value = "Failed to load item"
    console.error(e)
  } finally {
    loading.value = false
  }
})

const handleBuy = async () => {
  try {
    const response = await axios.get(`/api/buy/${route.params.id}/`)
    const session = response.data
    const stripe = await stripePromise
    
    const { error } = await stripe.redirectToCheckout({
      sessionId: session.id,
    })
    
    if (error) {
      console.error(error)
    }
  } catch (e) {
    console.error("Buy failed", e)
    alert("Buy failed")
  }
}
</script>

<template>
  <div class="item-container">
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else-if="item" class="item-card">
      <h1>{{ item.name }}</h1>
      <p>{{ item.description }}</p>
      <p class="price">
        Price: {{ (item.price / 100).toFixed(2) }} <span class="currency">{{ item.currency.toUpperCase() }}</span>
      </p>
      <button @click="handleBuy" class="buy-btn">Buy Now</button>
    </div>
  </div>
</template>

<style scoped>
.item-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
}
.item-card {
  border: 1px solid #ddd;
  padding: 2rem;
  border-radius: 8px;
  background: #f9f9f9;
}
.price {
  font-size: 1.2rem;
  font-weight: bold;
  margin: 1rem 0;
}
.currency {
  color: #666;
  font-size: 0.9rem;
}
.buy-btn {
  background-color: #5469d4;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}
.buy-btn:hover {
  background-color: #4456b1;
}
</style>
