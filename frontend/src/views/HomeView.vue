<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const items = ref([])
const loading = ref(true)
const error = ref(null)
const router = useRouter()

onMounted(async () => {
  try {
    const response = await axios.get('/api/items/')
    items.value = response.data
  } catch (e) {
    error.value = "Failed to load items"
    console.error(e)
  } finally {
    loading.value = false
  }
})

const goToItem = (id) => {
  router.push({ name: 'item', params: { id } })
}
</script>

<template>
  <div class="home-container">
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
    
    <div v-if="items.length === 0 && !loading">
        <p>No items found. Please add items via Admin Panel.</p>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}
.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}
.item-card {
  border: 1px solid #ddd;
  padding: 1.5rem;
  border-radius: 8px;
  background: #fff;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}
.item-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
.price {
  font-weight: bold;
  color: #5469d4;
  margin-top: 1rem;
}
</style>

