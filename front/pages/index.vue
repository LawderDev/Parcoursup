<template>
  <div>
    <NavBar name="M"></NavBar>
    <div class="flex justify-end mr-10">
      <ModalCreateSession @handle-validate="api_call_sessions"></ModalCreateSession>
    </div>
    <div class="mt-6">
      <SessionItem
        v-for="session in state.sessions"
        :title="session.nom"
        :endDate="'Fin le ' + session.end_date"
        @delete="openDeleteModal(session)"
        @handleClick="openSessionPage(session.id)"
      ></SessionItem>
    </div>
    <ModalDeleteSession v-model:isOpen="state.isOpen" :session-title="state.selectedSession.title" :session-id="state.selectedSession.id" @handle-delete="api_call_sessions"></ModalDeleteSession>
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
     // Axios instance configuration to include credentials (cookies)
     const axiosInstance = axios.create({
        baseURL: 'http://localhost:5000',
        withCredentials: true
      });

      // User registration
      axiosInstance.post('/api/register', {
        Nom: 'Test',
        Email: 'test@test10.com',
        Password: 'monMDP'
      }).then(response => {
        console.log(response.data);
      }).catch(error => {
        console.error(error.response.data);
      });

      // User login
      axiosInstance.post('/api/login', {
        Email: 'test@test10.com',
        Password: 'monMDP'
      }).then(response => {
        console.log(response.data);
        
        // Access protected route after login
        axiosInstance.get('/api/current_user')
          .then(response => {
            console.log(response.data);
          })
          .catch(error => {
            console.error(error.response.data);
          });
      }).catch(error => {
        console.error(error.response.data);
      });
  } catch (error) {
    console.error("Erreur lors de la récupération des sessions :", error);
  }
  state.isOpen = false
};

await api_call_sessions();
</script>
