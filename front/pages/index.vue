<template>
  <div>
    <NavBar name="M"></NavBar>
    <div class="flex justify-end mr-10">
      <ModalCreateSession></ModalCreateSession>
    </div>
    <div class="mt-6">
      <SessionItem v-for="session in state.sessions" :title="session.nom" :endDate="'Fin le ' + session.end_date" @delete="openDeleteModal" @handleClick="openSessionPage(session.id)"></SessionItem>
    </div>

    <div class="flex justify-center">
      <ButtonPlus class="md:hidden neumorphism"></ButtonPlus>
    </div>

    <ModalDeleteSession v-model:isOpen="state.isOpen" :session-title="state.selectedSession.title", :session-id="state.selectedSession.id"></ModalDeleteSession>
  </div>
</template> 

<script setup>
import { reactive } from "vue";
import axios from "axios";
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