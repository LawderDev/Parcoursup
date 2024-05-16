<template>
  <div>
    <!-- VERSION PAGE -->
    <div class="flex items-center" v-if="props.editMode">
      <h1 class="text-3xl font-bold max-w-48 md:max-w-96 truncate tooltip tooltip-open" data-tip="Projet TIC 2024"
        v-if="!state.editTitle">
        {{ state.sessionName }}
      </h1>
      <input v-model="state.newTitle" v-if="state.editTitle" class="input input-bordered my-8 font-bold" />
      <div class="ml-3 p-3 flex items-center grow">
        <EditTitle v-if="!state.editTitle" class="m-3" :src="Edit" @click="state.editTitle = true"></EditTitle>
        <EditTitle v-if="state.editTitle" :src="OkClickable" @click="handleEditOk"></EditTitle>
        <EditTitle v-if="state.editTitle" :src="Cancel" @click="handleEditCancel"></EditTitle>
        <ImageButton class="ml-auto" :src="Delete"></ImageButton>
      </div>
    </div>

    <!-- VERSION MODAL -->
    <div v-if="!props.editMode">
      <h2 class="mx-5 mb-2">Nom de la session</h2>
      <div class="flex w-full px-5 mb-5">
        <input v-model="state.sessionName" class="input input-bordered w-full rounded-badge" />
      </div>
    </div>

    <h2 class="mx-5 mb-2">Date de fin des formations des groupes</h2>
    <DateComponent v-model:endDate="state.endDateGroup" class="px-5 mb-5" />
    <h2 class="mx-5 mb-2">Date de fin de la session</h2>
    <DateComponent v-model:endDate="state.endDateSession" :endDateGroup="state.endDateGroup" class="px-5 mb-5" />
    <h2 class="mx-5 mb-2">Nombre de personnes par groupe</h2>
    <div class="md:w-13">
      <label class="input input-bordered flex items-center gap-4 mx-5 mb-2 rounded-badge">
        Minimum
        <input v-model="state.minGroup" type="number" class="grow" placeholder="Entrez un nombre" :min="0"
          :max="state.maxGroup" />
      </label>
      <label class="input input-bordered flex items-center gap-4 mx-5 mb-5 rounded-badge">
        Maximum
        <input v-model="state.maxGroup" type="number" class="grow" placeholder="Entrez un nombre" :min="state.minGroup"
          :max="9999" />
      </label>
    </div>

    <!-- VERSION MODAL UNIQUEMENT -->
    <div v-if="!props.editMode">
      <h2 class="mx-5 mb-2">Liste des étudiants</h2>
      <div class="mx-5">
        <FileInput acceptedTypes=".csv" @fileSelected="handleFileSelected" />
        <p v-if="state.selectedFile">
          Fichier sélectionné: {{ state.selectedFile.name }}
        </p>
      </div>
    </div>

    <div class="m-5">
      <div role="alert" class="flex alert alert-error max-w-50 justify-center items-center rounded-badge" id="alert"
        v-if="state.error && !formCorrect">
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span v-if="!fileCorrect" class="">Veuillez renseigner un fichier valide</span>
        <span v-else>Erreur inconnue.</span>
      </div>
    </div>

    <!-- VERSION PAGE -->
    <div class="flex place-content-between mt-8" v-if="props.editMode">
      <div class="hidden md:flex items-center p-4">
        <ButtonPrimary @click="handleClick" class="md:place-self-end place-start neumorphism">Enregistrer les
          modifications</ButtonPrimary>
      </div>
    </div>
    <div class="p-4 flex items-center justify-center z-50 md:hidden" v-if="props.editMode">
      <ButtonPrimary @click="handleClick" class="md:place-self-end place-start neumorphism">Enregistrer les
        modifications</ButtonPrimary>
    </div>

    <!-- VERSION MODAL -->
    <div class="p-4 flex items-center justify-center z-50 md:hidden" v-if="!props.editMode">
      <ButtonPrimary @click="handleClick" class="md:place-self-end place-start neumorphism">Valider
      </ButtonPrimary>
    </div>
    <div class="flex justify-center" v-if="!props.editMode">
      <div class="hidden md:flex p-4">
        <ButtonPrimary @click="handleClick" class="md:place-self-end place-start">Valider</ButtonPrimary>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from "vue";
import axios from "axios";
import Delete from "~/public/delete.svg";
import Edit from "~/public/edit.svg";
import OkClickable from "~/public/okClickable.svg";
import Cancel from "~/public/cancel.svg";

const props = defineProps({
  editMode: Boolean,
});

const state = reactive({
  sessionID: 1,
  editTitle: false,
  newTitle: null,
  sessionName: "Session",
  fileContent: null,
  minGroup: 1,
  maxGroup: null,
  endDate: null,
  endDateGroup: null,
  endDateSession: null,
  error: false,
});

watch(state, (newVal) => {
  if (!state.newTitle) {
    state.newTitle = state.sessionName;
  }
});

const handleEditOk = () => {
  state.sessionName = state.newTitle;
  state.editTitle = false;
};
const handleEditCancel = () => {
  state.editTitle = false;
};

const handleFileSelected = (file) => {
  state.fileContent = file;
};

let formCorrect = computed(() => {
  return fileCorrect.value && groupCorrect.value;
});
const fileCorrect = computed(() => {
  return state.fileContent != null;
});

const groupCorrect = computed(() => {
  return (
    state.minGroup != null &&
    state.maxGroup != null &&
    state.minGroup > 0 &&
    state.maxGroup > state.minGroup
  );
});


const handleClick = async () => {
  if (formCorrect.value) {
    state.error = false;

    if (!props.editMode) {
      const formData = {
        data: [{
          'Nom': state.sessionName,
          'Deadline_Creation_Groupe': state.endDateGroup,
          'Deadline_Choix_Projet': state.endDateSession,
          'Nb_Etudiant_Min': state.minGroup,
          'Nb_Etudiant_Max': state.maxGroup,
          'Etat': 'Choosing',
          'Fk_Utilisateur': 1,
        }
        ],
      };

      const jsonDataSession = JSON.stringify(formData);
      const session_id = await create_session(jsonDataSession);

      const jsonDataStudent = {
        session_ID: session_id,
        data: state.fileContent,
      };
      console.log(state.fileContent);

      //create_student(jsonDataStudent)


    } else if (props.editMode) {
      const formData = {
        data: [{
          'Nom': state.sessionName,
          'Session_id': state.session_ID,
          'Deadline_Creation_Groupe': state.endDateGroup,
          'Deadline_Choix_Projet': state.endDateSession,
          'Nb_Etudiant_Min': state.minGroup,
          'Nb_Etudiant_Max': state.maxGroup,
          'Etat': 'Choosing',
          'Fk_Utilisateur': 1,
        }
        ],
      };

      const jsonDataSession = JSON.stringify(formData);
      const session_id = await update_session(jsonDataSession);

    }

  } else {
    state.error = true;
  }
};

const create_session = async (jsonData) => {
  try {
    const res = await axios.post(
      "http://127.0.0.1:5000/api/create_session",
      jsonData,
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    return res.data.result[0];
  } catch (err) {
    console.error(err);
  }
};

const create_student = async (jsonData) => {
  try {
    const res = await axios.post(
      "http://127.0.0.1:5000/api/create_student",
      jsonData,
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    return res
  } catch (err) {
    console.error(err);
  }
};

const update_session = async (jsonData) => {
  try {
    const res = await axios.post(
      "http://127.0.0.1:5000/api/update_session",
      jsonData,
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    return res.data.result[0];
  } catch (err) {
    console.error(err);
  }
};
</script>
