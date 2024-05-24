<template>
  <div>
    <Modal @close="$emit('update:isOpen', false)">
      <template v-slot:open-btn>
        <div class="flex items-center button" @click="emit">
          <img src="../public/settings.svg" class="w-5" />
          <a class="md:text-lg pl-2">Profil</a>
        </div>
      </template>
      <template v-slot:form>
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
        </div>
        <div>
          <h3 class="text-center m-1">Voulez-vous changer de mot de passe?</h3>
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
const openBtn = ref(null);

const state = reactive({
  name: "Benois-Pineau",
  firstname: "Jenny",
  email: "jbenoispineau@u-bordeaux.fr",
});
const emit = defineEmits(["update:isOpen"]);
const handleDisplayProfile = () => {
  // Votre logique pour afficher le profil
};
</script>
