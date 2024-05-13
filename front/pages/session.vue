<template>
  <div>
    <NavBar :name="'fdsf'" />
    <div class="grid m-8 mx-10">
      <h1 class="text-3xl my-8 font-bold">Projet TIC 2024</h1>
      <ImageButton src="~/public/delete.svg"></ImageButton>
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
      <h2 class="text-xl my-8 font-semibold">Date de fin</h2>
      <DateComponent
        :selectedDate="state.endDate"
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
        <span v-if="!projectCorrect" class="">Veuillez renseigner au moins un projet</span>
        <span v-else-if="!fileCorrect" class=""
          >Veuillez renseigner un fichier valide</span
        >
        <span v-else-if="!groupCorrect"
          >Veuillez renseigner des groupes valides</span
        >
        <span v-else-if="!dateCorrect"
          >Veuillez renseigner une date de fin valide</span
        >
        <span v-else
          >Erreur inconnue.</span
        >
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
      <h3 class="ml-5 text-gray-500">Quels seront les projets disponibles ?</h3>
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
      <div class="grid grid-cols-1 md:grid-cols-4 mb-20 md:mb-0">
        <div v-for="item in liste" :key="item.id">
          <ProjectCard :title="item.title" :summary="item.summary" />
        </div>
      </div>
    </div>
    <!-- Boutons en bas de l'écran -->
  </div>
</template>

<script setup>
import { reactive } from "vue";
import DateComponent from "~/components/Date.vue";
import NavBar from "~/components/NavBar.vue";
import FileInput from "~/components/FileInput.vue";
import ButtonPrimary from "~/components/ButtonPrimary.vue";
import ProjectCard from "~/components/ProjectCard.vue";
import ButtonPlus from "~/components/ButtonPlus.vue";
import ImageButton from "~/components/ImageButton.vue";

const state = reactive({
  selectedFile: null,
  file: null,
  minGroup: 1,
  maxGroup: null,
  endDate: null,
  project: [""],
  error: false,
});
const handleDateSelected = (selectedDate) => {
  state.endDate = selectedDate;
};
const handleFileSelected = (file) => {
  state.selectedFile = file;
};

let formCorrect = computed(() => {
  return (
    fileCorrect.value &&
    dateCorrect.value &&
    groupCorrect.value &&
    projectCorrect.value
  );
});
const projectCorrect = computed(() => {
  return state.project != null && state.project.length > 0;
});
const fileCorrect = computed(() => {
  return state.selectedFile != null;
});
const dateCorrect = computed(() => {
  return state.endDate != null && new Date(state.endDate) >= new Date();
});
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
  } else {
    state.error = true;
  }
};
const liste = [
  {
    id: 1,
    title: "Titre de l'élément 1",
    summary:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed quis ex non mauris vehicula scelerisque. Ut in ex ac nulla auctor dictum. Quisque volutpat vulputate risus, non scelerisque justo porta a. Phasellus auctor nisl vel tincidunt consequat. Suspendisse potenti. Nullam vestibulum malesuada faucibus. Suspendisse ac tortor lectus. Maecenas in pulvinar felis. Sed sit amet augue nec orci tincidunt lacinia. Vivamus euismod, metus ac convallis feugiat, libero elit auctor libero, nec vestibulum justo libero a dolor. Fusce efficitur libero eu justo suscipit, vitae finibus mi bibendum. Cras vulputate elit et lacus ultricies, vitae placerat enim vestibulum.",
  },
  {
    id: 2,
    title: "Titre de l'élément 2",
    summary:
      "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Integer id lorem sit amet purus ultrices consequat at et libero. Duis ultricies quam vitae diam scelerisque sollicitudin. Maecenas fermentum justo vel dui sodales dapibus. Etiam nec nulla vel odio aliquet facilisis. Vivamus ut est a enim consectetur consectetur. Nulla facilisi. Vivamus bibendum ultricies mi, nec suscipit felis malesuada ac. Ut tempus justo sapien, eu tincidunt turpis iaculis vel. Ut et magna nec libero commodo venenatis nec nec mauris. Nam eget vehicula odio, ut mattis ipsum. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Ut dapibus dui sed quam fermentum, sed fermentum lorem porttitor. Integer nec vestibulum lacus. Proin varius tempus velit, ut rhoncus mi varius id. Integer tristique leo nec velit fringilla, sed vehicula nunc rhoncus.",
  },
  {
    id: 3,
    title: "Titre de l'élément 3",
    summary:
      "Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Integer ut arcu ac est tempor malesuada. Morbi lacinia nulla nec justo feugiat, ac convallis odio auctor. Nulla in turpis lorem. Nam non nibh fermentum, lobortis mi ut, consequat nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Integer volutpat vestibulum lorem, id accumsan lorem efficitur sit amet. Morbi laoreet euismod elit, ut egestas eros aliquet eget. Integer auctor eros in mi facilisis vehicula. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Curabitur venenatis sem id massa rutrum, nec interdum eros auctor. Fusce non sapien nec justo consequat viverra. Integer aliquet, enim eget mattis ultricies, velit ipsum vulputate metus, eget pharetra justo tortor non odio. Aliquam rutrum nisi vel urna dapibus, sed fringilla velit suscipit. Aliquam erat volutpat. Cras vel metus nulla. Nam sed elit tincidunt, finibus lorem sit amet, lacinia ipsum.",
  },
  {
    id: 4,
    title: "Titre de l'élément 3",
    summary:
      "Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Integer ut arcu ac est tempor malesuada. Morbi lacinia nulla nec justo feugiat, ac convallis odio auctor. Nulla in turpis lorem. Nam non nibh fermentum, lobortis mi ut, consequat nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Integer volutpat vestibulum lorem, id accumsan lorem efficitur sit amet. Morbi laoreet euismod elit, ut egestas eros aliquet eget. Integer auctor eros in mi facilisis vehicula. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Curabitur venenatis sem id massa rutrum, nec interdum eros auctor. Fusce non sapien nec justo consequat viverra. Integer aliquet, enim eget mattis ultricies, velit ipsum vulputate metus, eget pharetra justo tortor non odio. Aliquam rutrum nisi vel urna dapibus, sed fringilla velit suscipit. Aliquam erat volutpat. Cras vel metus nulla. Nam sed elit tincidunt, finibus lorem sit amet, lacinia ipsum.",
  },
  {
    id: 5,
    title: "Titre de l'élément 3",
    summary:
      "Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Integer ut arcu ac est tempor malesuada. Morbi lacinia nulla nec justo feugiat, ac convallis odio auctor. Nulla in turpis lorem. Nam non nibh fermentum, lobortis mi ut, consequat nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Integer volutpat vestibulum lorem, id accumsan lorem efficitur sit amet. Morbi laoreet euismod elit, ut egestas eros aliquet eget. Integer auctor eros in mi facilisis vehicula. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Curabitur venenatis sem id massa rutrum, nec interdum eros auctor. Fusce non sapien nec justo consequat viverra. Integer aliquet, enim eget mattis ultricies, velit ipsum vulputate metus, eget pharetra justo tortor non odio. Aliquam rutrum nisi vel urna dapibus, sed fringilla velit suscipit. Aliquam erat volutpat. Cras vel metus nulla. Nam sed elit tincidunt, finibus lorem sit amet, lacinia ipsum.",
  },
];
</script>
