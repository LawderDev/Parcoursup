<template>
  <div>
    <h1
      class="text-3xl font-bold w-[100vw] h-[100vh] flex items-center justify-center"
    >
      {{ state.helloWorld }}
    </h1>
    <Modal>
      <template v-slot:open-btn>
        <ButtonPrimary title="Créer une session"></ButtonPrimary>
      </template>
      <template v-slot:form>
        <div class="flex flex-col">
          <h1 class="font-semibold text-primary text-center mb-5 text-xl">Créer une session</h1>
          <div class="text-secondary">
            <form method="dialog">
              <h2 class="mb-2">Nom de la session</h2>
              <input
                type="text"
                placeholder="Tapez ici"
                class="input input-bordered w-full max-w-xs mb-4"
              />
              <h2 class="mb-2">Date de fin de la session</h2>
              <Date class="mb-4"></Date>

              <h2 class="mb-2">Sélectionner le fichier des étudiants</h2>
              <input
                type="file"
                class="file-input file-input-bordered w-full max-w-xs mb-4"
              />

              <h2 class="mb-2">Nombre de personnes par groupe :</h2>
              <h3 class="mb-1">Min</h3>
              <input type="number" value="0" min="1" max="100" class="input input-bordered max-w-xs" />
              <h3 class="mb-1">Max</h3>
              <input type="number" value="0" min="1" max="100" class="input input-bordered max-w-xs mb-4"/>
              <div class="flex justify-center">
                <ButtonPrimary title="Valider"></ButtonPrimary>
              </div>
              <button class="btn btn-sm btn-circle btn-ghost absolute left-2 top-2">
                ✕
              </button>
            </form>
          </div>
        </div>
      </template>
    </Modal>
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
