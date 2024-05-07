<template>
  <div>
   <h1 class="text-3xl font-bold w-[100vw] h-[100vh] flex items-center justify-center"> {{ state.helloWorld }} </h1>
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
    state.helloWorld = response.data;
  } catch (error) {
    console.error("Error fetching hello world:", error);
  }
};

fetchHelloWorld();
</script>
