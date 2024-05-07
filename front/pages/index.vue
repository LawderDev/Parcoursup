<template>
  <div>
    <NavBar name="M"></NavBar>
    <div class="flex justify-end mr-10">
      <ButtonPrimary>Ajouter un projet</ButtonPrimary>
    </div>
    <div class="mt-6">
      <SessionItem title="Projet TIC 2024" endDate="Fin de 12/05/2024"></SessionItem>
      <SessionItem title="Projet TIC 2023" endDate="Fin de 12/05/2024"></SessionItem>
      <SessionItem title="Projet TIC 2022" endDate="Fin de 12/05/2024"></SessionItem>
      <SessionItem title="Projet TIC 2021" endDate="Fin de 12/05/2024"></SessionItem>
      <SessionItem title="Projet TIC 2020" endDate="Fin de 12/05/2024"></SessionItem>
    </div>
    <div class="flex justify-center">
      <ButtonPlus class="md:hidden neumorphism"></ButtonPlus>
    </div>

    <Modal @handle-submit="handleSubmit">
      <template v-slot:open-btn>
        <ButtonPrimary title="Créer une session"></ButtonPrimary>
      </template>
      <template v-slot:form>
        <div class="flex flex-col">
          <h1 class="font-semibold text-primary text-center mb-5 text-xl">
            Créer une session
          </h1>
          <div class="text-secondary">
            <form method="dialog">
              <h2 class="mb-2">Nom de la session</h2>
              <input
                v-model="state.sessionName"
                type="text"
                placeholder="Tapez ici"
                class="input input-bordered w-full max-w-xs mb-4"
              />
              <h2 class="mb-2">Date de fin des inscriptions des groupes</h2>
              <Date class="mb-4" v-model="state.endDateGroup"></Date>

              <h2 class="mb-2">Date de fin de la session</h2>
              <Date class="mb-4" v-model="state.endDateSession"></Date>

              <h2 class="mb-2">Sélectionner le fichier des étudiants</h2>
              <input
                type="file"
                class="file-input file-input-bordered w-full max-w-xs mb-4"
                @change="handleFileInput"
              />

              <h2 class="mb-2">Nombre de personnes par groupe :</h2>
              <div class="flex">
                <div class="flex flex-col w-[45%] mr-[10%]">
                  <h3 class="mb-1">Min</h3>
                  <input
                    id="min"
                    type="number"
                    value="0"
                    min="0"
                    :max="state.groupeMax"
                    class="input input-bordered"
                    @change="handleMinMaxChange('min', $event)"
                  />
                </div>
                <div class="flex flex-col w-[45%]">
                  <h3 class="mb-1">Max</h3>
                  <input
                    id="max"
                    type="number"
                    value="1"
                    min="0"
                    :min="state.minValue"
                    max="100"
                    class="input input-bordered"
                    @change="handleMinMaxChange('max', $event)"
                  />
                </div>
              </div>
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
/*const state = reactive({
  helloWorld: "",
  sessionName: "",
  fileName: "",
  endDateGroup: "",
  endDateSession: "",
  maxValue: "",
  minValue: "",
  fileContent: "",
});

const fetchHelloWorld = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:5000/api/hello_world");
    state.helloWorld = response.data;
  } catch (error) {
    console.error("Error fetching hello world:", error);
  }
};

fetchHelloWorld();*/

const handleSubmit = () => {

};
</script>
