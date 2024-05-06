<template>
  <div>
    <NavBar></NavBar>
    <div class="flex justify-end mr-10">
      <ButtonPrimary title = "Ajouter un projet"> </ButtonPrimary>
    </div>
    <div class="mt-6">
      <SessionItem title = "Projet TIC 2024" endDate = "Fin de 12/05/2024"></SessionItem>
      <SessionItem title = "Projet TIC 2023" endDate = "Fin de 12/05/2024"></SessionItem>
      <SessionItem title = "Projet TIC 2022" endDate = "Fin de 12/05/2024"></SessionItem>
      <SessionItem title = "Projet TIC 2021" endDate = "Fin de 12/05/2024"></SessionItem>
      <SessionItem title = "Projet TIC 2020" endDate = "Fin de 12/05/2024"></SessionItem>
    </div>
    <div class="flex justify-center">
      <ButtonPlus class="md:hidden neumorphism"></ButtonPlus>
    </div>
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
});

const fetchHelloWorld = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:5000/api/hello_world");
    state.helloWorld = response.data;
  } catch (error) {
    console.error("Error fetching hello world:", error);
  }
};

fetchHelloWorld();
</script>
