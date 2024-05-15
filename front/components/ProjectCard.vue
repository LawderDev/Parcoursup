<template>
  <div>
    <Card class="m-5">
      <h1 class="text-xl">{{props.name}}</h1>
      <p class="my-5 max-h-32 text-ellipsis overflow-auto">{{props.summary}}</p>
      <div>
        <ButtonSecondary @click="handleClickModify" class="mr-2 my-2">Modifier</ButtonSecondary>
        <ButtonPrimary>Vos préférences</ButtonPrimary>
      </div>
    </Card>
  </div>
</template>
<script setup>
const props = defineProps(['name','summary'])

const emit  = defineEmits(["modifyProject"]);

const handleClickModify = () => {
  console.log("modifyProfect");
  emit("modifyProject",{name:props.name, summary:props.summary});
}
</script>
