<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { loadStripe } from '@stripe/stripe-js'

const route = useRoute()
const loading = ref(true)
const error = ref(null)
const order = ref(null) // We don't have an Order detail API yet, but let's assume we might need one or just buy by ID

// For this task, since we don't have a full Order Detail API (GET /order/{id}), 
// we can't easily show the order details before buying unless we implement it.
// BUT, the task asked to implement "Order model... and payment on total cost".
// Let's assume for the view we just show a "Pay Order #ID" button or try to fetch details if we add the endpoint.
// I'll add a simple Order Detail API endpoint to Django first to make this view useful.

const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLIC_KEY || 'pk_test_placeholder')

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
    }
  } catch (e) {
    console.error("Buy failed", e)
    alert("Buy failed or Order not found")
  }
}
</script>

<template>
  <div class="container">
    <h1>Order #{{ route.params.id }}</h1>
    <p>Ready to pay for your order?</p>
    <button @click="handleBuyOrder" class="pay-btn">Pay for Order</button>
  </div>
</template>

<style scoped>
.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}
.pay-btn {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 18px;
  margin-top: 20px;
}
.pay-btn:hover {
  background-color: #218838;
}
</style>

