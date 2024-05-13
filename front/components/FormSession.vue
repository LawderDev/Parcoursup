<template>
  <div>
    <div class="flex items-center">
      <h1 class="text-3xl my-8 font-bold max-w-48 md:max-w-96 truncate tooltip tooltip-open" data-tip="Projet TIC 2024 ffffffffffffffffffffffffff" v-if="!state.editTitle">{{state.sessionName}}</h1>
      <input 
        v-model="state.newTitle" 
        v-if="state.editTitle" 
        class="input input-bordered  my-8 font-bold"
      >
      <div class="ml-3 p-3 flex items-center grow">
        <EditTitle v-if="!state.editTitle" class="m-3" :src="Edit" @click="state.editTitle=true"></EditTitle>
        <EditTitle v-if="state.editTitle" :src="OkClickable" @click="handleEditOk" ></EditTitle>
        <EditTitle v-if="state.editTitle" :src="Cancel" @click="handleEditCancel" ></EditTitle>
        <ImageButton class="ml-auto" :src="Delete"></ImageButton>
      </div>
    </div>

    <h2 class="text-xl my-4 font-semibold">Liste des étudiants</h2>
    <h3 class="ml-5 text-gray-500">
      Entrez la liste des participants au format .csv
    </h3>
    <FileInput
      class="my-5"
      acceptedTypes=".csv"
      @fileSelected="handleFileSelected"
    />
    <p v-if="state.selectedFile">
      Fichier sélectionné: {{ state.selectedFile.name }}
    </p>
    <h2 class="text-xl my-8 font-semibold">Nombre de personnes par groupe</h2>
    <div class="md:w-13">
      <label
        class="input input-bordered flex items-center gap-4 m-4 rounded-badge"
      >
        Minimum
        <input
          v-model="state.minGroup"
          type="number"
          class="grow"
          placeholder="Entrez un nombre"
          :min="0"
          :max="state.maxGroup"
        />
      </label>
      <label
        class="input input-bordered flex items-center gap-4 m-4 rounded-badge"
      >
        Maximum
        <input
          v-model="state.maxGroup"
          type="number"
          class="grow"
          placeholder="Entrez un nombre"
          :min="state.minGroup"
          :max="9999"
        />
      </label>
    </div>
    <h2 class="text-xl my-8 font-semibold">
      Date de fin des formations des groupes
    </h2>
    <DateComponent
      :selectedDate="state.endDateGroup"
      @newDateSelected="handleDateSelected"
      class="px-5"
    />
    <h2 class="text-xl my-8 font-semibold">Date de fin de la session</h2>
    <DateComponent
      :selectedDate="state.endDateSession"
      @newDateSelected="handleDateSelected"
      class="px-5"
    />
    <div
      role="alert"
      class="flex alert alert-error my-4 max-w-50 justify-center items-center"
      id="alert"
      v-if="state.error && !formCorrect"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="stroke-current shrink-0 h-6 w-6"
        fill="none"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
        />
      </svg>
      <span v-if="!fileCorrect" class=""
        >Veuillez renseigner un fichier valide</span
      >
      <span v-else-if="!groupCorrect"
        >Veuillez renseigner des groupes valides</span
      >
      <span v-else-if="!dateCorrect"
        >Veuillez renseigner une date de fin valide</span
      >
      <span v-else>Erreur inconnue.</span>
    </div>
    <div class="flex place-content-between mt-8">
      <h2 class="text-xl mt-8 mb-4 font-semibold">Projets</h2>
      <div class="hidden md:flex items-center p-4">
        <ButtonPlus class="mr-5 neumorphism" />
        <ButtonPrimary
          @click="handleClick"
          class="md:place-self-end place-start neumorphism"
          >Enregistrer les modifications</ButtonPrimary
        >
      </div>
    </div>
    <div
      class="sticky inset-x-0 bottom-1 p-4 flex items-center justify-center z-50 md:hidden"
    >
      <ButtonPlus class="mr-5 neumorphism" />
      <ButtonPrimary
        @click="handleClick"
        class="md:place-self-end place-start neumorphism"
        >Enregistrer les modifications</ButtonPrimary
      >
    </div>
  </div>
</template>

<script setup>
import { reactive } from "vue";
import Delete from "~/public/delete.svg";
import Edit from "~/public/edit.svg";
import OkClickable from "~/public/okClickable.svg";
import Cancel from "~/public/cancel.svg";

const state = reactive({
  editTitle : false,
  newTitle : null,
  sessionName: "Session111111111111111",
  fileContent: null,
  minGroup: 1,
  maxGroup: null,
  endDateGroup: null,
  endDateSession: null,
  error: false,
});

const handleEditOk = () => {
  state.sessionName = state.newTitle;
  state.editTitle = false;
}
const handleEditCancel = () => {
  state.editTitle = false;
}
const handleDateSelected = (selectedDate) => {
  state.endDate = selectedDate;
};
const handleFileSelected = (file) => {
  state.fileContent = file;
};

let formCorrect = computed(() => {
  return fileCorrect.value && dateCorrect.value && groupCorrect.value;
});
const fileCorrect = computed(() => {
  return state.fileContent != null;
});
const dateCorrect = computed(() => {
  return state.endDate != null && new Date(state.endDate) >= new Date();
});


watch(state, (newVal) => {
  console.log("newVal",newVal);
  if(!state.newTitle){
    state.newTitle=state.sessionName;
  }
})


const groupCorrect = computed(() => {
  return (
    state.minGroup != null &&
    state.maxGroup != null &&
    state.minGroup > 0 &&
    state.maxGroup > state.minGroup
  );
});
const handleClick = () => {
  if (formCorrect.value) {
    console.log("valid form");
    state.error = false;
    console.log(state.fileContent);
    const formData = {
      sessionName: state.sessionName,
      endDateGroup: state.endDateGroup,
      endDateSession: state.endDateSession,
      minGroup: state.minValue,
      maxGroup: state.maxValue,
    };

    console.log(formData);
    const jsonData = JSON.stringify(formData);
  } else {
    state.error = true;
  }
};
</script>
