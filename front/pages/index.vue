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
import axios from "axios";
const state = reactive({
  helloWorld: "",
  isOpen: false,
});

const data = { 
        "data" : [
            {'Nom': "test",
            'Deadline_Creation_Groupe':'12/02/2024', 
            'Deadline_Choix_Projet':'12/04/2024',
            'Nb_Etudiant_Min':4,
            'Nb_Etudiant_Max':5,
            'FK_Utilisateur':1,
            }
        ]     
        };
const jsonData = JSON.stringify(data);

const response = await axios.post("http://127.0.0.1:5000/api/create_session", jsonData, {
  headers: {
    'Content-Type': 'application/json'
  }}
);

const openDeleteModal = () => {
  console.log("open delete modal");
  state.isOpen = true;
};
</script>