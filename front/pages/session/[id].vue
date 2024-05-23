<template>
  <div>
    <NavBar :name="'fdsf'" />
    <div class="my-8 mx-32">
      <FormSession editMode v-if="stateSession.session" :session-data="stateSession.session" @handle-end-session="handleEndSession"></FormSession>
      <div>
        <div class="flex items-center mt-5 mb-5">
          <h2 class="text-3xl font-semibold mr-5">Projets</h2>
          <ModalProjectForm
            v-if="stateSession.session"
            v-model:isOpen="state.isOpen"
            :editMode="state.editMode"
            v-model:name="state.name"
            v-model:summary="state.summary"
            v-model:id="state.id"
            :session-state="stateSession.session.state"
            @submit:project="handleNewProject"
            @modify:project="handleModifyProject"
            @create:project="openCreateModal"
          >
        </ModalProjectForm>
        </div>
        <h3 class="ml-5 text-gray-500">
          Quels seront les projets disponibles ?
        </h3>
        <div
          class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 mb-20 md:mb-0"
        >
          <div v-for="project in stateProject.projects" :key="project.id">
            <ProjectCard
              @modifyProject="openModifyModal"
              @deleteProject="handleDeleteProject"
              @handleClickPreferencies="handleClickPreferencies"
              :id="project.id"
              :name="project.nom"
              :summary="project.description"
              :session-state="stateSession.session.state"
            />
          </div>
        </div>
      </div>
      <RankingGroupModal
        v-model:isOpen="state.isRankingGroupModalOpen"
        :project-id="state.selectedProjectId"
        :session-id="Number(route.params.id)"
      ></RankingGroupModal>
    </div>
    <!-- Boutons en bas de l'écran -->
  </div>
</template>

<script setup>
import { useRoute } from "vue-router";
import axios from "axios";
import { onMounted } from "vue";
import { useSessionData } from "~/composables/useSessionData";
import { useProject } from "~/composables/useProject";

const state = reactive({
  editMode: false,
  name: null,
  summary: null,
  isOpen: false,
  isRankingGroupModalOpen: false,
  selectedProjectId: 0,
  loading: false,
});

const { stateProject, api_call_projects } = useProject();
const { stateSession, getSessionData } = useSessionData();

const handleDeleteProject = async (id) => {
  try {
    await axios.post("http://127.0.0.1:5000/api/delete_project", {
      projectID: id,
    });
    await api_call_projects(sessionID);
  } catch (error) {
    console.error("Erreur lors de la suppression de la session", error);
  }
};

const create_project = async (jsonData) => {
  try {
    const res = await axios.post(
      "http://127.0.0.1:5000/api/create_project",
      jsonData,
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    await api_call_projects(sessionID);
    return res;
  } catch (err) {
    console.error(err.response);
  }
};
const update_project = async (jsonData) => {
  try {
    const res = await axios.post(
      "http://127.0.0.1:5000/api/update_project",
      jsonData,
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    await api_call_projects(sessionID);
    return res;
  } catch (err) {
    console.error(err.response);
  }
};
const handleNewProject = async (newProject) => {
  const formData = {
    data: [
      {
        Nom: newProject.name,
        Description: newProject.summary,
        Nb_Etudiant_Min: null,
        Nb_Etudiant_Max: null,
        FK_Session: route.params.id,
      },
    ],
  };
  const jsonDataSession = JSON.stringify(formData);
  const project_id = await create_project(jsonDataSession);
};
const handleModifyProject = async (newProject) => {
  const formData = {
    data: [
      {
        id: newProject.id,
        nom: newProject.name,
        description: newProject.summary,
        min_etu: null,
        max_etu: null,
        id_session: route.params.id,
      },
    ],
  };
  console.log(formData);
  const jsonDataSession = JSON.stringify(formData);
  const project_id = await update_project(jsonDataSession);
};

const handleClickPreferencies = (projectId) => {
  state.selectedProjectId = Number(projectId);
  state.isRankingGroupModalOpen = true;
};

const openCreateModal = () => {
  state.isOpen = true;
  state.editMode = false;
  state.name = null;
  state.summary = null;
};
const openModifyModal = (event) => {
  state.isOpen = true;
  state.editMode = true;
  state.id = event.id;
  state.name = event.name;
  state.summary = event.summary;
};

const route = useRoute();
const sessionID = route.params.id;

definePageMeta({
  validate: async (route) => {
    const api_check_id = async (sessionID) => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/api/get_session_id?sessionID=" + sessionID
        );

        if (!response.data || response.data.length == 0) {
          return false;
        } else {
          return true;
        }
      } catch (error) {
        console.error("Erreur lors de la récupération des sessions :", error);
      }
    };
    return (
      typeof route.params.id === "string" &&
      /^\d+$/.test(route.params.id) &&
      api_check_id(route.params.id)
    );
  },
});

const handleEndSession = async () => {
  stateSession.session.state = "Attributing";
};

onMounted(async () => {
  await getSessionData(sessionID);
  await api_call_projects(sessionID);
});

</script>
