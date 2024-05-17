<template>
  <div>
    <NavBar :name="'fdsf'" />
    <div class="grid justify-center m-8">
      <FormSession editMode></FormSession>
      <div>
        <div class="flex items-center mt-5 mb-5">
          <h2 class="text-3xl font-semibold mr-5">Projets</h2>
          <ModalProjectForm
            v-model:isOpen="state.isOpen"
            :editMode="state.editMode"
            v-model:name="state.name"
            v-model:summary="state.summary"
            v-model:id="state.id"
            @submit:project="handleNewProject"
            @modify:project="handleModifyProject"
            @create:project="openCreateModal"
          >
          </ModalProjectForm>
          <ButtonPrimary class="ml-auto">Assigner les projets</ButtonPrimary>
        </div>
        <h3 class="ml-5 text-gray-500">
          Quels seront les projets disponibles ?
        </h3>
        <div
          class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3  mb-20 md:mb-0"
        >
          <div v-for="project in state.projects" :key="project.id">
            <ProjectCard
              @modifyProject="openModifyModal"
              @deleteProject="handleDeleteProject"
              :id="project.id"
              :name="project.nom"
              :summary="project.description"
            />
          </div>
        </div>
      </div>
    </div>
    <!-- Boutons en bas de l'écran -->
  </div>
</template>

<script setup>
import axios from "axios";
const state = reactive({
  editMode: false,
  name: null,
  summary: null,
  isOpen: false,
  projects: [],
  selectedSession: {
    id: 1,
    title: "test",
    endDate: "test",
  },
});

const handleDeleteProject = async (id) => {
  try {
    await axios.post("http://127.0.0.1:5000/api/delete_project", {
      projectID: id,
    });
    await api_call_projects();
  } catch (error) {
    console.error("Erreur lors de la suppression de la session", error);
  }
};
const api_call_projects = async () => {
  try {
    const data = {
      sessionID: state.selectedSession.id,
    };
    const jsonData = JSON.stringify(data);
    const response = await axios.post(
      "http://127.0.0.1:5000/api/get_all_projects",
      jsonData,
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    state.projects = response.data;
  } catch (error) {
    console.error("Erreur lors de la récupération des project :", error);
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
    await api_call_projects();
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
    await api_call_projects();
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
        FK_Session: state.selectedSession.id,
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
        id_session: state.selectedSession.id,
      },
    ],
  };
  const jsonDataSession = JSON.stringify(formData);
  const project_id = await update_project(jsonDataSession);
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
  state.id = event.id
  state.name = event.name;
  state.summary = event.summary;
};
await api_call_projects();
</script>
