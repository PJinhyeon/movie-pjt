<template>
  <div class="sort-toggle">
    <select v-model="selectedSort" @change="emitSortChange">
      <option v-for="option in sortOptions" :key="option.value" :value="option.value">
        {{ option.label }}
      </option>
    </select>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue';

const emit = defineEmits(['sortChanged']);
const selectedSort = ref('latest');

const sortOptions = [
  { value: 'latest', label: '최신순' },
  { value: 'oldest', label: '오래된 순' },
  { value: 'ascending', label: '오름차순' },
  { value: 'descending', label: '내림차순' }
];

const emitSortChange = () => {
  emit('sortChanged', selectedSort.value);
};
</script>

<style scoped>
.sort-toggle {
  margin-bottom: 20px;
}

select {
  padding: 5px;
  font-size: 1rem;
}
</style>