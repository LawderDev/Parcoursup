<template>
  <div>
    <NavBar></NavBar>
    <template v-if="state.isLoading">
      <div class="flex justify-end mr-10">
        <ModalCreateSession @handle-validate="api_call_sessions"></ModalCreateSession>
      </div>
      <div class="mt-6">
        <SessionItem
          v-for="session in state.sessions"
          :title="session.nom"
          :end-date="'Fin le ' + format_date(session.end_date)"
          :session-state="session.state"
          @delete="openDeleteModal(session)"
          @handleClick="openSessionPage(session.id)"
        ></SessionItem>
      </div>
      <ModalDeleteSession hide-button v-model:isOpen="state.isOpen" :session-title="state.selectedSession.title" :session-id="state.selectedSession.id" @handle-delete="api_call_sessions"></ModalDeleteSession>
    </template>
    <Skeleton v-else></Skeleton>
  </div>
</template>

<script setup>
import { reactive } from "vue";
import axios from "axios";

const config = useRuntimeConfig();

const state = reactive({
  helloWorld: "",
  isOpen: false,
  selectedSession: {},
  sessions: [],
  isLoading: false
});

const openDeleteModal = (session) => {
  state.selectedSession.id = session.id;
  state.selectedSession.title = session.nom;
  state.selectedSession.endDate = session.end_date;
  state.isOpen = true;
};

const openSessionPage = async (sessionID) => {
  await navigateTo("/session/" + sessionID);
};

const api_call_sessions = async () => {
  try {
    const response = await axios.get(`${config.public.backUrl}/api/get_sessions`);
    state.sessions = response.data
  } catch (error) {
    console.error("Erreur lors de la récupération des sessions :", error);
  }
  state.isOpen = false
};

const format_date = (dateString) => {
  const date = new Date(dateString);

  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-based
  const year = date.getFullYear();

  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');

  return `${day}/${month}/${year} à ${hours}h${minutes}`;
}

onMounted(async () => {
  await api_call_sessions();
  state.isLoading = true;
})


</script>
