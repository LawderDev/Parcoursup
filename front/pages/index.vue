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
import axios from "axios";
import { reactive } from "vue";
// Petite subtilité , c'est mieux de faire ça que ref,
// ça évite de créer une variable à chaque fois
// quand les gens débutent ils utilisent toujours ref
// mais en réalité ref est plus utilisé pour autre chose :D

// Tout ce qui sera dans l'objet state du coup sera reactif !
const state = reactive({
  helloWorld: "",
  isOpen: false,
});

const data = {
  "project":["Parcoursup","La desc", 5, 6, 1]
};
const jsonData = JSON.stringify(data);

const response = await axios.post("http://127.0.0.1:5000/api/create_project", jsonData, {
  headers: {
    'Content-Type': 'application/json'
  }}
);

const openDeleteModal = () => {
  console.log("open delete modal");
  state.isOpen = true;
};
</script>