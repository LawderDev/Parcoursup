<template>
  <div>
    <!-- VERSION PAGE -->
    <template v-if="props.editMode">
      <div class="flex justify-between flex-wrap items-start gap-4 mb-4">
          <ButtonPrimary
            v-if="state.sessionState === 'Grouping'"
            class="btn-wide"
            @click="handleGrouping"
            >Vérifier les groupes</ButtonPrimary
          >
          <ButtonPrimary
            v-else-if="state.sessionState === 'Choosing'"
            class="btn-wide"
            @click="handleEndSession"
            >Terminer la session</ButtonPrimary
          >
          <ButtonPrimary
            v-else-if="state.sessionState === 'Attributing'"
            class="btn-wide"
            @click="handleAssignProjects"
            >Assigner les projets</ButtonPrimary
          >
          <div class="btn" v-if="state.sessionState === 'Grouping'" @click="copyLink(`${config.public.frontUrl}/createGroup/${state.sessionID}`)">
            http://localhost:3000/createGroup/{{ state.sessionID }}
            <img alt="copy-svg" src="../public/copy.svg" class="h-6 w-6" />
          </div>
          <div v-else @click="downloadGroups">
            <ButtonSecondary>Télécharger la composition des groupes</ButtonSecondary>
          </div>
        </div>
    </template>
    <div class="flex items-center" v-if="props.editMode">
      <h2
        class="text-3xl font-bold max-w-48 md:max-w-96 truncate tooltip tooltip-open"
        v-show="!state.editTitle"
      >
        {{ state.sessionName }}
      </h2>
      <input
        v-model="state.newTitle"
        v-if="state.editTitle"
        class="input input-bordered my-8 font-bold max-w-40 md:max-w-48"
      />
      <div class="ml-3 flex items-center grow">
        <EditInput
          v-show="!state.editTitle"
          class="m-3"
          :src="Edit"
          @click="state.editTitle = true"
        ></EditInput>
        <EditInput
          v-show="state.editTitle && state.newTitle.length"
          :src="OkClickable"
          @click="handleEditOk"
        ></EditInput>
        <EditInput
          v-show="state.editTitle"
          :src="Cancel"
          @click="handleEditCancel"
        ></EditInput>
        <div class="ml-auto flex gap-4">
          <div v-if="props.editMode">
            <div class="hidden md:flex">
              <ButtonPrimary
                v-if="state.sessionState === 'Attributing'"
                class="md:place-self-end place-start"
                disabled
                >Enregistrer les modifications</ButtonPrimary
              >
              <ButtonPrimary
                v-else
                @click="handleClick"
                class="md:place-self-end place-start"
                >Enregistrer les modifications</ButtonPrimary
              >
          </div>
        </div>
          <ModalDeleteSession
            v-model:isOpen="state.isOpen"
            :session-title="state.sessionName"
            :session-id="state.sessionID"
            @handle-delete="handleDelete"
          ></ModalDeleteSession>
        </div>
      </div>
    </div>

    <!-- VERSION MODAL -->
    <div v-if="!props.editMode">
      <h2 class="mb-2">Nom de la session</h2>
      <div class="flex w-full mb-5">
        <input
          v-model="state.sessionName"
          class="input input-bordered w-full rounded-badge"
        />
      </div>
    </div>

    <!--- DATE FORM --->
    <div :class="{'md:flex md:flex-wrap md:gap-4': props.editMode}">
      <div>
        <h2 class="mb-2">Date de fin des formations des groupes</h2>
        <DateComponent v-if="props.editMode && (state.sessionState !== 'Grouping')" v-model="state.endDateGroup" class="mb-5" disabled/>
        <DateComponent v-else class="mb-5" v-model="state.endDateGroup" />
      </div>
    
      <div>
        <h2 class="mb-2">Date de fin de la session</h2>
        <DateComponent v-if="props.editMode && (state.sessionState === 'Attributing')" v-model="state.endDateSession" class="mb-5" disabled/>
        <DateComponent v-else v-model="state.endDateSession" class="mb-5" />
      </div>
    </div>
    <!--- GROUP FORM --->
    <h2 class="mb-2">Nombre de personnes par groupe</h2>
    <div class="md:w-13" :class="{'md:flex md:items-center md:flex-wrap gap-4': props.editMode}">
      <label class="input input-bordered flex items-center gap-4 rounded-badge">
        Minimum
        <input
          v-if="props.editMode && state.sessionState !== 'Grouping'"
          v-model="state.minGroup"
          type="number"
          class="grow"
          :class="{'w-[150px]': props.editMode}"
          placeholder="Entrez un nombre"
          :min="0"
          :max="state.maxGroup"
          disabled
        />
        <input
          v-else
          v-model="state.minGroup"
          type="number"
          class="grow"
          :class="{'w-[150px]': props.editMode}"
          placeholder="Entrez un nombre"
          :min="0"
          :max="state.maxGroup"
        />
      </label>
      <label class="input input-bordered flex items-center gap-4 my-5 rounded-badge">
        Maximum
        <input
          v-if="props.editMode && state.sessionState !== 'Grouping'"
          v-model="state.maxGroup"
          type="number"
          class="grow input-size"
          :class="{'w-[150px]': props.editMode}"
          placeholder="Entrez un nombre"
          :min="state.minGroup"
          :max="9999"
          disabled
        />
        <input
          v-else
          v-model="state.maxGroup"
          type="number"
          class="grow"
          :class="{'w-[150px]': props.editMode}"
          placeholder="Entrez un nombre"
          :min="state.minGroup"
          :max="9999"
        />
      </label>
    </div>

    <!-- VERSION MODAL UNIQUEMENT -->
    <div v-if="!props.editMode">
      <h2 class="mb-2">Liste des étudiants</h2>
      <div>
        <FileInput acceptedTypes=".csv" @fileSelected="handleFileSelected" />
        <p v-if="state.selectedFile">
          Fichier sélectionné: {{ state.selectedFile.name }}
        </p>
      </div>
    </div>

    <!-- VERSION PAGE -->

    <div
      class="p-4 flex items-center justify-center z-50 md:hidden"
      v-if="props.editMode"
    >
      <ButtonPrimary
        v-if="state.sessionState === 'Attributing'"
        class="md:place-self-end place-start"
        disabled
        >Enregistrer les modifications</ButtonPrimary
      >
      <ButtonPrimary
        v-else
        @click="handleClick"
        class="md:place-self-end place-start"
        >Enregistrer les modifications</ButtonPrimary
      >
    </div>

    <!-- VERSION MODAL -->
    <div
      class="p-4 flex items-center justify-center z-50 md:hidden"
      v-if="!props.editMode"
    >
      <ButtonPrimary
        @click="handleClick"
        class="md:place-self-end place-start neumorphism"
        >Valider
      </ButtonPrimary>
    </div>
    <div class="flex justify-center" v-if="!props.editMode">
      <div class="hidden md:flex p-4">
        <ButtonPrimary @click="handleClick" class="md:place-self-end place-start"
          >Valider</ButtonPrimary
        >
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
import { useSessionData } from "~/composables/useSessionData";
import { useToasterStore } from "~/stores/toaster";
import ButtonSecondary from "./ButtonSecondary.vue";
import { useGroups } from "@/composables/useGroups";

const props = defineProps({
  editMode: Boolean,
  sessionData: Object,
});

const config = useRuntimeConfig();

const { stateGroups, getAllGroups } = useGroups();

const route = useRoute();

const toaster = useToasterStore();

const { updateSession } = useSessionData();

const emit = defineEmits(["handleValidate", "handleEndSession"]);

const state = reactive({
  sessionID: null,
  editTitle: false,
  newTitle: null,
  sessionName: null,
  sessionState: "",
  fileContent: null,
  minGroup: 1,
  maxGroup: null,
  endDateGroup: null,
  endDateSession: null,
  error: false,
  isOpen: false,
});

watch(
  () => state.editTitle,
  () => {
    if (state.editTitle) {
      state.newTitle = state.sessionName;
    }
  }
);

onMounted(() => {
  if (props.sessionData) {
    state.sessionName = props.sessionData.name_session;
    state.sessionState = props.sessionData.state;
    state.minGroup = props.sessionData.group_min;
    state.maxGroup = props.sessionData.group_max;
    state.endDateGroup = new Date(props.sessionData.end_date_group);
    state.endDateSession = new Date(props.sessionData.end_date_session);
    state.sessionID = props.sessionData.id;
  }
});

const handleDelete = async () => {
  await navigateTo("/");
};

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
  return dateCorrect.value && groupCorrect.value && nameCorrect.value;
});

const groupCorrect = computed(() => {
  return (
    state.minGroup != null &&
    state.maxGroup != null &&
    state.minGroup > 0 &&
    state.maxGroup > state.minGroup
  );
});

const nameCorrect = computed(() => {
  return state.sessionName != null;
});

const dateCorrect = computed(() => {
  const today = new Date();
  return true /* (
    state.endDateGroup < state.endDateSession &&
    state.endDateGroup > today &&
    state.endDateGroup != null &&
    state.endDateSession != null
  ); */
});

const handleClick = async () => {
  if (formCorrect.value) {
    state.error = false;
    if (!props.editMode) {
      //MODAL
      const formData = {
        data: [
          {
            Nom: state.sessionName,
            Deadline_Creation_Groupe: state.endDateGroup,
            Deadline_Choix_Projet: state.endDateSession,
            Nb_Etudiant_Min: state.minGroup,
            Nb_Etudiant_Max: state.maxGroup,
            Etat: "Grouping",
            FK_Utilisateur: 1,
          },
        ],
      };

      const jsonDataSession = JSON.stringify(formData);
      const session_id = await create_session(jsonDataSession);
      
      if (session_id) {
        const dictStudent = {
          sessionID: session_id,
          data: state.fileContent.data,
        };

        const jsonDataStudent = JSON.stringify(dictStudent);
        const std_id = await create_student(jsonDataStudent);
        await sendCreateGroupMail(session_id);
        toaster.showMessage("La session a bien été crée", "success");
        emit("handleValidate");
      } else {
        toaster.showMessage("Erreur lors de la création de la session", "error");
        console.error("Probleme de session id : ", session_id);
      }
    } else if (props.editMode) {
      //UPDATE
      const formData = {
        session_ID: state.sessionID,
        data: [
          {
            Nom: state.sessionName,
            Deadline_Creation_Groupe: state.endDateGroup,
            Deadline_Choix_Projet: state.endDateSession,
            Nb_Etudiant_Min: state.minGroup,
            Nb_Etudiant_Max: state.maxGroup,
            Etat: state.sessionState,
            FK_Utilisateur: 1,
          },
        ],
      };
      const jsonDataSession = JSON.stringify(formData);
      const session_id = await updateSession(jsonDataSession);

      session_id ? toaster.showMessage("La session a bien été modifiée", "success") : toaster.showMessage("Erreur lors de la modification de la session", "error");
      emit("handleValidate");
    }
  } else {
    state.error = true;
    if(!nameCorrect.value){
      toaster.showMessage("Veuillez respecter les contraintes de nom", "error");
    }
    else if(!dateCorrect.value){
      toaster.showMessage("Veuillez respecter les contraintes de dates", "error");
    }
    else if(!groupCorrect.value){
      toaster.showMessage("Veuillez respecter les contraintes de groupes", "error");
    }else {
      toaster.showMessage("Erreur lors de la création de la session", "error");
    }
  }
};

const sendCreateGroupMail = async (session_id) => {
  //TODO SEND MAIL CREATE GROUP TO ALL STUDENTS
  /*try {
    const res = await axios.post(`${config.public.backUrl}/api/send_create_group_mail`, {
      session_id: session_id,
    });
    return res;
  } catch (err) {
    console.error(err);
  }*/
};

const create_session = async (jsonData) => {
  try {
    const res = await axios.post(`${config.public.backUrl}/api/create_session`, jsonData, {
      headers: {
        "Content-Type": "application/json",
      },
    });
    return res.data.result[0];
  } catch (err) {
    console.error(err);
  }
};

const create_student = async (jsonData) => {
  try {
    const res = await axios.post(`${config.public.backUrl}/api/create_students`, jsonData, {
      headers: {
        "Content-Type": "application/json",
      },
    });
    return res;
  } catch (err) {
    console.error(err);
  }
};

const handleEndSession = async () => {
  const formData = {
    session_ID: state.sessionID,
    data: [
      {
        Nom: props.sessionData.name_session,
        Deadline_Creation_Groupe: props.sessionData.end_date_group,
        Deadline_Choix_Projet: props.sessionData.end_date_session,
        Nb_Etudiant_Min: props.sessionData.group_min,
        Nb_Etudiant_Max: props.sessionData.group_max,
        Etat: "Attributing",
        FK_Utilisateur: 1,
      },
    ],
  };

  const jsonDataSession = JSON.stringify(formData);
  const res = await updateSession(jsonDataSession);
  if(res) {
    state.sessionState = "Attributing";
    emit("handleEndSession");
    toaster.showMessage("La session a bien été cloturée", "success");
  }else {
    toaster.showMessage("Erreur lors de la clôturation de la session", "error");
  }
};

const handleGrouping = async () => {
  await navigateTo(`/validateGroup/${state.sessionID}`);
};

const handleAssignProjects = async () => {
  await navigateTo(`/result/${state.sessionID}`);
};

const copyLink = (link) => {
  navigator.clipboard.writeText(link);
  toaster.showMessage("Lien copié dans le presse-papier", "success");
};

const downloadGroups = async() => {
     await getAllGroups(state.sessionID);
     stateGroups.groups = stateGroups.groups.sort((a, b) => a.id - b.id);

     let content = `Nom de la session: ${state.sessionName}\n`;
     content += `ID de la session:: ${state.sessionID}\n\n`;
     stateGroups.groups.forEach((group, index) => {
      content += `---------------------------------------------------------------------------\n`;
      content += `Groupe ${index + 1}\n`;
      content += `Lien du choix des préférences: http://localhost:3000/rankingProjects/${state.sessionID}/${group.id}\n\n`;

      content += `Composition du groupe:\n\n`;
      group.students.forEach(student => {
          content += `Nom: ${student.name}, Prénom: ${student.firstname}, Email: ${student.email}\n`;
      });
     })
     
     console.log(content)

    // Crée un Blob avec le contenu texte
    const blob = new Blob([content], { type: 'text/plain' });

    // Crée un lien de téléchargement
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'groupes.txt';

    // Ajoute le lien au document et clique dessus pour démarrer le téléchargement
    document.body.appendChild(link);
    link.click();

    // Supprime le lien du document
    document.body.removeChild(link);
  }
</script>
