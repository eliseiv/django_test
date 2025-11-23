<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const items = ref([])
const orders = ref([])
const loading = ref(true)
const error = ref(null)
const router = useRouter()

onMounted(async () => {
  try {
    const [itemsRes, ordersRes] = await Promise.all([
      axios.get('/api/items/'),
      axios.get('/api/orders/')
    ])
    items.value = itemsRes.data
    orders.value = ordersRes.data
  } catch (e) {
    error.value = "Failed to load data"
    console.error(e)
  } finally {
    loading.value = false
  }
})

const goToItem = (id) => {
  router.push({ name: 'item', params: { id } })
}

const goToOrder = (id) => {
  router.push({ name: 'order', params: { id } })
}
</script>

<template>
  <div class="home-container">
    
    <!-- Items Section -->
    <section>
      <h1>Available Items</h1>
      <div v-if="loading">Loading...</div>
      <div v-else-if="error">{{ error }}</div>
      
      <div v-else class="items-grid">
        <div v-for="item in items" :key="item.id" class="item-card" @click="goToItem(item.id)">
          <h2>{{ item.name }}</h2>
          <p>{{ item.description }}</p>
          <p class="price">
              {{ (item.price / 100).toFixed(2) }} {{ item.currency.toUpperCase() }}
          </p>
        </div>
      </div>
      
      <div v-if="items.length === 0 && !loading" class="empty-state">
          <p>No items found. Please add items via Admin Panel.</p>
      </div>
    </section>

    <!-- Orders Section -->
    <section class="orders-section">
      <h1>Pending Orders</h1>
      <div v-if="!loading && orders.length > 0" class="items-grid">
        <div v-for="order in orders" :key="order.id" class="order-card" @click="goToOrder(order.id)">
          <h2>Order #{{ order.id }}</h2>
          <p>{{ order.items.length }} items</p>
          <p v-if="order.discount" class="badge discount">Discount: {{ order.discount }}%</p>
          <p v-if="order.tax" class="badge tax">Tax: {{ order.tax }}%</p>
        </div>
      </div>
      <div v-if="orders.length === 0 && !loading" class="empty-state">
          <p>No orders found. Create them in Admin Panel to test bulk payment.</p>
      </div>
    </section>

  </div>
</template>

<style scoped>
.home-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
}
section {
  margin-bottom: 3rem;
}
.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 1.5rem;
}
.item-card, .order-card {
  border: 1px solid #e0e0e0;
  padding: 1.5rem;
  border-radius: 12px;
  background: #fff;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}
.order-card {
  border-left: 5px solid #5469d4;
}
.item-card:hover, .order-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.08);
}
.price {
  font-weight: bold;
  color: #5469d4;
  margin-top: 1rem;
  font-size: 1.2em;
}
.empty-state {
  color: #666;
  font-style: italic;
}
.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.85em;
  margin-right: 5px;
  margin-top: 5px;
}
.discount {
  background: #e8f5e9;
  color: #2e7d32;
}
.tax {
  background: #fff3e0;
  color: #ef6c00;
}
</style>
