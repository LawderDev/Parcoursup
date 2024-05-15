<template>
  <div>
    <NavBar name="M"></NavBar>
    <div class="flex justify-end mr-10">
      <ModalCreateSession></ModalCreateSession>
      <ButtonPrimary>Ajouter un projet</ButtonPrimary>
    </div>
    <div class="mt-6">
      <SessionItem title="Projet TIC 2024" endDate="Fin le 12/05/2024" @delete="openDeleteModal"></SessionItem>
      <SessionItem title="Projet TIC 2022" endDate="Fin le 12/05/2024" @delete="openDeleteModal"></SessionItem>
      <SessionItem title="Projet TIC 2021" endDate="Fin le 12/05/2024" @delete="openDeleteModal"></SessionItem>
      <SessionItem title="Projet TIC 2020" endDate="Fin le 12/05/2024" @delete="openDeleteModal"></SessionItem>
    </div>

    <div class="flex justify-center">
      <ButtonPlus class="md:hidden neumorphism"></ButtonPlus>
    </div>

    <ModalDeleteSession v-model:isOpen="state.isOpen"></ModalDeleteSession>
  </div>
</template> 

<script setup>
import { reactive } from "vue";
const state = reactive({
  helloWorld: "",
  isOpen: false,
});

const openDeleteModal = () => {
  console.log("open delete modal");
  state.isOpen = true;
};
</script>