<template>
  <div>
    <Card class="m-5">
      <h1 class="text-xl">{{props.title}}</h1>
      <p class="my-5 max-h-32 text-ellipsis overflow-auto">{{props.summary}}</p>
      <div>
        <ButtonSecondary class="mr-2 ">Modifier</ButtonSecondary>
        <ButtonPrimary>Vos préférences</ButtonPrimary>
      </div>
    </Card>
  </div>
</template>
<script setup>
import ButtonPrimary from "~/components/ButtonPrimary.vue";
import ButtonSecondary from "~/components/ButtonSecondary.vue";
import Card from "~/components/Card.vue";
const props = defineProps(['title','summary'])
</script>
