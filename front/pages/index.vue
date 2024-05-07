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
                v-model="state.sessionName"
                type="text"
                placeholder="Tapez ici"
                class="input input-bordered w-full max-w-xs mb-4"
              />
              {{ state.sessionName }}
              <h2 class="mb-2">Date de fin de la session</h2>
              <Date class="mb-4" v-model="state.endDate"></Date>
              {{  state.endDate }}


              <h2 class="mb-2">Sélectionner le fichier des étudiants</h2>
              <input
                type="file"
                class="file-input file-input-bordered w-full max-w-xs mb-4"
                @change="handleFileInput"
              />
              {{ state.fileName }}

              <h2 class="mb-2">Nombre de personnes par groupe :</h2>
              <div class="flex"> 
                <div class="flex flex-col w-[45%] mr-[10%]">
                  <h3 class="mb-1">Min</h3>
                  <input type="number" value="0" min="1" max="100" class="input input-bordered"/>
                </div>
                <div class="flex flex-col w-[45%]">
                  <h3 class="mb-1">Max</h3>
                  <input type="number" value="0" min="1" max="100" class="input input-bordered"/>
                </div>
              </div>
              <div class="flex justify-center mt-5">
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
  sessionName: "",
  fileName: "",
  endDate: "",
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

const handleFileInput = (event) => {
  const files = event.target.files;
  console.log(files)
    // Now you can do something with the selected files
    // For example, you can access the first file's name like this:
    if (files.length > 0) {
      state.fileName = files[0].name;
      
    } else {
      state.fileName = ''; // No file selected
    }
}
</script>
