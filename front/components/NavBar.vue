<template>
  <div>
    <div
      class="flex justify-between items-center navbar-center bg-base-100 shadow-lg rounded-badge m-4 p-5 px-8"
    >
      <div>
        <div class="avatar">
          <div class="w-16 rounded-xl">
            <button @click="redirectToIndex">
              <img src="../public/logo.png" alt="logo" />
            </button>
          </div>
        </div>
      </div>
      <div>
        <button @click="redirectToIndex">
          <h1 class="text-xl md:block">Smart Choice</h1>
        </button>
      </div>
      <div class="dropdown dropdown-end">
        <div tabindex="0" role="button" class="btn btn-ghost btn-circle">
          <div class="avatar placeholder">
            <div class="bg-primary text-neutral-content rounded-full w-12">
              <span v-if="letter" class="text-xl uppercase">{{ letter }}</span>
            </div>
          </div>
        </div>
        <ul
          tabindex="0"
          class="shadow menu menu-lg md:menu-sm dropdown-content bg-base-100 rounded-box w-60 z-20"
        >
        <ModalProfile></ModalProfile>
          <li class="pl-1">
            <div class="flex items-center">
              <img src="../public/users.svg" class="w-5" />
              <NuxtLink class="md:text-lg" to="/users">Utilisateurs</NuxtLink>
            </div>
          </li>
          <li class="pl-1">
            <div class="flex items-center" @click="handleDisconnect">
              <img src="../public/logout.svg" class="w-5" />
              <a class="md:text-lg">Deconnexion</a>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
<script setup>
import ModalProfile from './ModalProfile.vue';
import { useToasterStore } from "~/stores/toaster";
import axios from 'axios';
import ModalProfile from './ModalProfile.vue';

const letter = computed(() => props.name.charAt(0));
const toaster = useToasterStore();

const state = reactive({
  name: "Maabout",
})

const letter = computed(() => state.name.charAt(0));

const redirectToIndex = async () => {
  await navigateTo(`/`);
};
const redirectToConnexion = async () => {
  await navigateTo(`/connexion`);
};
const handleDisconnect = async() => {
  await callLogout()
  toaster.showMessage("Deconnexion réussie", "success");
  redirectToConnexion();
}
const callLogout = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:5000/api/logout", {
      withCredentials: true, // Ensure cookies are sent and received
    });
  } catch (error) {
    console.error("Erreur lors de la deconnexion :", error);
  }
}
</script>
