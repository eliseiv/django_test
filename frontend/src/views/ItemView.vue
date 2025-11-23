<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { loadStripe } from '@stripe/stripe-js'

const route = useRoute()
const router = useRouter()
const item = ref(null)
const loading = ref(true)
const error = ref(null)

const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLIC_KEY)

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

const handleBuySession = async () => {
  try {
    const response = await axios.get(`/api/buy/${route.params.id}/`)
    const session = response.data
    const stripe = await stripePromise
    
    const { error } = await stripe.redirectToCheckout({
      sessionId: session.id,
    })
    
    if (error) {
      console.error(error)
      alert("Stripe Error: " + error.message)
    }
  } catch (e) {
    console.error(e)
    alert("Something went wrong: " + e.message)
  }
}

const handleBuyIntent = () => {
  router.push({ name: 'pay-intent', params: { id: item.value.id } })
}
</script>

<template>
  <div class="container" v-if="item">
    <h1>{{ item.name }}</h1>
    <p class="price">{{ item.price / 100 }} {{ item.currency.toUpperCase() }}</p>
    <p>{{ item.description }}</p>
    
    <div class="actions">
      <button @click="handleBuySession" class="buy-btn">Buy (Checkout Session)</button>
      <button @click="handleBuyIntent" class="buy-btn intent-btn">Buy (Payment Intent)</button>
    </div>
  </div>
  <div v-else-if="loading">Loading...</div>
  <div v-else-if="error">{{ error }}</div>
</template>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
.price {
  font-size: 1.5em;
  font-weight: bold;
  color: #2c3e50;
}
.actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}
.buy-btn {
  background: #42b983;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 1.2em;
  cursor: pointer;
  border-radius: 4px;
}
.intent-btn {
  background: #5469d4; /* Stripe Blue */
}
</style>
