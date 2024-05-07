<template>
  <div class="card w-70 md:w-80 bg-base-100 neumorphism">
    <div class="card-body">
      <h2 class="card-title">{{ props.title }}</h2>
      <p>{{props.summary}}</p>
      <div class="card-actions justify-end">
        <button class="btn btn-primary">Buy Now</button>
      </div>
    </div>
  </div>
</template>
<script setup> 
import ButtonPrimary from "~/components/ButtonPrimary.vue";
const props = defineProps(["title","summary"]);
</script>