<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { loadStripe } from '@stripe/stripe-js'

const route = useRoute()
const router = useRouter()
const loading = ref(true)
const error = ref(null)
const clientSecret = ref(null)
const stripeInstance = ref(null)
const elements = ref(null)

onMounted(async () => {
  try {
    // 1. Get the Payment Intent Client Secret and Public Key from Backend
    const response = await axios.get(`/api/buy/intent/${route.params.id}/`)
    const { clientSecret: secret, publicKey } = response.data
    
    clientSecret.value = secret
    
    // 2. Initialize Stripe with the correct key for this currency
    stripeInstance.value = await loadStripe(publicKey)
    
    // 3. Create Elements
    elements.value = stripeInstance.value.elements({ clientSecret: secret })
    const paymentElement = elements.value.create('payment')
    paymentElement.mount('#payment-element')
    
  } catch (e) {
    error.value = "Failed to load payment form"
    console.error(e)
  } finally {
    loading.value = false
  }
})

const handleSubmit = async () => {
  if (!stripeInstance.value || !elements.value) {
    return
  }
  
  loading.value = true
  
  const { error: stripeError } = await stripeInstance.value.confirmPayment({
    elements: elements.value,
    confirmParams: {
      return_url: window.location.origin + '/success',
    },
  })

  if (stripeError) {
    error.value = stripeError.message
    loading.value = false
  } else {
    // Redirect happens automatically
  }
}
</script>

<template>
  <div class="payment-container">
    <h1>Complete your payment</h1>
    
    <div v-if="error" class="error">{{ error }}</div>
    
    <form id="payment-form" @submit.prevent="handleSubmit">
      <div id="payment-element">
        <!-- Stripe Elements will insert the payment form here -->
      </div>
      
      <button id="submit" :disabled="loading || !clientSecret" class="pay-button">
        <span v-if="loading">Processing...</span>
        <span v-else>Pay Now</span>
      </button>
    </form>
  </div>
</template>

<style scoped>
.payment-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
}

.error {
  color: red;
  margin-bottom: 20px;
}

.pay-button {
  margin-top: 20px;
  width: 100%;
  padding: 12px;
  background-color: #5469d4;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

.pay-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>

