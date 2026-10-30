<script setup>
defineProps({
  errors: { type: Array, default: () => [] },
});
</script>

<template>
  <ul v-if="errors.length" class="form-errors" role="alert">
    <li v-for="error in errors" :key="error">{{ error }}</li>
  </ul>
</template>

<style scoped>
.form-errors { color: #e55; margin: 0; padding-left: 20px; }
</style>
