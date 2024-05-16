<template>
  <div>
    <NavBar name="M"></NavBar>
    <div class="flex justify-end mr-10">
      <ModalCreateSession></ModalCreateSession>
    </div>
    <div class="mt-6">
      <SessionItem v-for="session in state.sessions" :title="session.nom" :endDate="'Fin le ' + session.end_date" @delete="openDeleteModal" @click="openSessionPage(session.id)"></SessionItem>
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
  sessions: [],
});

const openDeleteModal = () => {
  console.log("open delete modal");
  state.isOpen = true;
};

const openSessionPage = async(sessionID) => {
  console.log("open session page " + sessionID);
  await navigateTo('/session/' + sessionID)
}

const api_call_sessions = async () => {
  try {

    const response = await axios.get("http://127.0.0.1:5000/api/get_sessions");
    state.sessions = response.data
    console.log(state.sessions);

  } catch (error) {
    console.error(
      "Erreur lors de la récupération des sessions :",
      error
    );
  }
};


await api_call_sessions()
</script>