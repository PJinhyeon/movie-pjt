<template>
  <div>
    <div class="cart-item-list">
      <CartItem 
        v-if="token"
        v-for="cartItem in cart.cartItems" 
        :key="cartItem.id" 
        :cartItem="cartItem" 
      />
    </div>
  </div>
</template>

<script setup>
import CartItem from '@/components/CartItem.vue';
import { useCartStore } from '@/stores/cart';
import { onMounted, ref } from 'vue';

const cart = useCartStore()
const token = ref(localStorage.getItem('authToken'))

onMounted(() => {
  if (token.value) {
    cart.getCart(); // 토큰이 있을 때만 호출
  } else {
    console.log("토큰이 없습니다. 로그인하세요.");
  }
})
</script>

<style scoped>
/* 페이지 제목 */
.page-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #FFE474; /* 강조된 노란색 */
  margin-bottom: 20px;
}

/* cart-item-list 컨테이너 */
.cart-item-list {
  display: flex;
  flex-wrap: wrap; /* 자식 요소들이 가로로 정렬되며 공간이 부족하면 줄바꿈 */
  gap: 20px; /* 아이템 간의 간격 */
  justify-content: flex-start; /* 왼쪽 정렬 */
  align-items: flex-start;
}
</style>
