<template>
    <StudentsActions 
      title="SELECTION"
      :nb-steps="2"
      :nb-steps-active="2"
      :nb-steps-lock="0"
      sub-title="Renseignez les informations pour permettre de créer votre demande de projet"
      button-title="Valider les préférences"
      @handle-button-click="validateRanking">
        <Ranking :items="state.projects" description="Classez les projets en fonction de vos préférences"></Ranking>
      </StudentsActions>
  </template>
  
  <script setup>
  import axios from "axios";

  const state = reactive({
    projects : [],
  })

  const route = useRoute()

  const getProjects = async () => {
    try {
      const data = {
        sessionID: route.params.sessionId,
        groupID: route.params.groupId
      };
      const jsonData = JSON.stringify(data);
      const response = await axios.post(
      "http://127.0.0.1:5000/api/get_group_projects_order_by_preferencies", 
      jsonData,
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    state.projects = response.data;
    console.log(state.projects)
  } catch (error) {
    console.error("Erreur lors de la récupération des project :", error);
  }
};

const setGroupPreferencies = async () => {
  try {
    const data = {
        "data": []
    }

    state.projects.forEach((project, index) => {
      data.data.push({
        "groupID": route.params.groupId,
        "projectID": project.id,
        "order": index,
      })
    })

    const jsonData = JSON.stringify(data);

    const response = await axios.post(
      "http://127.0.0.1:5000/api/affect_preference_group",
      jsonData,
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
  } catch (error) {
    console.error("Erreur lors de la création du groupe :", error);
  }
};
  
  
const validateRanking = async () => {
  await setGroupPreferencies();
  await navigateTo(`/rankingProjectsConfirmation/${route.params.sessionId}/${route.params.groupId}`)
}

await getProjects();
  
  </script>
  