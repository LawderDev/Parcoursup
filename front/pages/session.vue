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
          class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 mb-20 md:mb-0"
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
const handleDeleteProject = async (id) => {
  console.log("id",id)
  try {
    await axios.post("http://127.0.0.1:5000/api/delete_project", {
      projectID: id,
    });
    await api_call_projects();
  } catch (error) {
    console.error("Erreur lors de la suppression de la session", error);
  }
};
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
    console.log(state.projects);
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
const handleNewProject = async (newProject) => {
  console.log("handleNewProject", newProject);
  const formData = {
    data: [
      {
        Nom: "fdsfsdfs",
        Description: "desc",
        Nb_Etudiant_Min: null,
        Nb_Etudiant_Max: null,
        FK_Session: 1,
      },
    ],
  };
  const jsonDataSession = JSON.stringify(formData);
  const project_id = await create_project(jsonDataSession);

  console.log(project_id);
};
const handleModifyProject = (newProject) => {
  console.log("handleModifyProject", newProject);
};
const openCreateModal = () => {
  console.log("openCreateModal");
  state.isOpen = true;
  state.editMode = false;
  state.name = null;
  state.summary = null;
};
const openModifyModal = (event) => {
  console.log("openModifyModal", event.name);
  console.log("openModifyModal", event.summary);
  state.isOpen = true;
  state.editMode = true;
  state.name = event.name;
  state.summary = event.summary;
};
await api_call_projects();
</script>
