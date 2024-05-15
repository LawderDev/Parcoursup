<template>
  <div>
    <NavBar name="M"></NavBar>
    <div class="flex justify-end mr-10">
      <ModalCreateSession></ModalCreateSession>
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

    <ModalDeleteSession v-model:isOpen="state.isOpen" :session-title="state.selectedSession.title", :session-id="state.selectedSession.id"></ModalDeleteSession>
  </div>
</template> 

<script setup>
import { reactive } from "vue";
const state = reactive({
  helloWorld: "",
  isOpen: false,
  selectedSession: {
    id: 1,
    title: "test",
    endDate: "test",
  },
});

const openDeleteModal = () => {
  state.isOpen = true;
};
</script>