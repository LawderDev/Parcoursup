<template>
  <div>
    <Modal @close="$emit('update:isOpen', false)">
      <template v-slot:open-btn>
        <li class="pl-1 button">
          <div class="flex items-center">
            <img src="../public/settings.svg" class="w-5" />
            <a class="md:text-lg">Profil</a>
          </div>
        </li>
      </template>
      <template v-slot:form>
        <div class="m-5">
          <div class="flex justify-center">
            <h1 class="text-2xl text-primary">Profil</h1>
          </div>
          <div>
            <div>
              <h2 class="m-3">Nom</h2>
              <input
                v-model="state.name"
                type="text"
                class="input input-bordered w-full max-w-xs"
              />
            </div>
            <div>
              <h2 class="m-3">Prénom</h2>
              <input
                v-model="state.firstname"
                type="text"
                class="input input-bordered w-full max-w-xs"
              />
            </div>
            <div>
              <h2 class="m-3">Email</h2>
              <input
                v-model="state.email"
                type="text"
                class="input input-bordered w-full max-w-xs"
              />
            </div>
            <div>
              <h2 v-if="!state.editPassword" class="m-3">Mot de passe</h2>
              <h2 v-else class="m-3">Ancien mot de passe</h2>
              <input
                v-model="state.password"
                type="password"
                class="input input-bordered w-full max-w-xs"
              />
            </div>
            <div v-if="state.editPassword">
              <h2 class="m-3">Nouveau mot de passe</h2>
              <input
                v-model="state.newPassword"
                type="password"
                class="input input-bordered w-full max-w-xs"
              />
            </div>
            <div class="label" v-if="state.editPassword">
              <span class="label-text-alt">Le mot de passe doit etre différent du précedent et contenir au moins 8 caractères</span>
            </div>
          </div>
          <div class="flex justify-center mt-2">
            <EditTitle
              v-show="state.editPassword && state.newPassword.length"
              :src="OkClickable"
              @click="handleSubmitNewPassword"
            ></EditTitle>
            <EditTitle
              v-show="state.editPassword"
              :src="Cancel"
              @click="handleEditCancel"
            ></EditTitle>
          </div>
          <div class="mt-4" v-if="!state.editPassword">
            <h3 class="text-center m-1">
              Voulez-vous changer de
              <a class="link" @click="handleEditPassword">mot de passe?</a>
            </h3>
          </div>
        </div>
      </template>
      <template v-slot:action>
        <!-- Ajouter les boutons d'action ici si nécessaire -->
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { reactive } from "vue";
import { defineEmits } from "vue";

import OkClickable from "~/public/okClickable.svg";
import Cancel from "~/public/cancel.svg";

const state = reactive({
  name: "Benois-Pineau",
  firstname: "Jenny",
  email: "jbenoispineau@u-bordeaux.fr",
  password: "monMDP",
  newPassword: "",
  editPassword: false,
});
const emit = defineEmits(["update:isOpen"]);
const handleSubmitNewPassword = () => {
  if (passwordCorrect.value) {
    state.password = state.newPassword;
    state.newPassword = "";
  }
};
const handleEditPassword = () => {
  state.editPassword = true;
};
const handleEditCancel = () => {
  state.editPassword = false;
  state.newPassword = "";
};
const passwordCorrect = computed(() => {
  return state.password !== state.newPassword && state.newPassword.length >= 8;
});
</script>
