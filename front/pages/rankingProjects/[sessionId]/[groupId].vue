<template>
  <StudentsActions
    v-if="state.isLoading"
    title="SÉLECTION"
    :timestamp="state.timestamp"
    :nb-steps="2"
    :nb-steps-active="2"
    :nb-steps-lock="0"
    sub-title="Renseignez les informations pour permettre l'assignation des projets en fonction de vos préférences"
    button-title="Valider les préférences"
    @handle-button-click="validateRanking"
  >
    <Ranking
      :items="state.projects"
      description="Classez les projets en fonction de vos préférences"
    ></Ranking>
  </StudentsActions>
  <Skeleton v-else></Skeleton>
</template>

<script setup>
import axios from "axios";

const state = reactive({
  projects: [],
  timestamp: null,
  isLoading: false,
});

const config = useRuntimeConfig();

const route = useRoute();

definePageMeta({
  middleware: ["check-end-date-session"], // Pass parameters here
});

const getProjects = async () => {
  try {
    const data = {
      sessionID: route.params.sessionId,
      groupID: route.params.groupId,
    };
    const jsonData = JSON.stringify(data);
    const response = await axios.post(
      `${config.public.backUrl}/api/get_group_projects_order_by_preferencies`,
      jsonData,
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    state.projects = response.data;
    state.timestamp = response.data[0].date_derniere_modif
  } catch (error) {
    console.error("Erreur lors de la récupération des project :", error);
  }
};

const setGroupPreferencies = async () => {
  try {
    const data = {
      data: [],
    };
    const options = {
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "numeric",
      minute: "numeric",
    };

    state.projects.forEach((project, index) => {
      data.data.push({
        groupID: route.params.groupId,
        projectID: project.id,
        order: index + 1,
        Date_Derniere_Modif: new Date().toLocaleDateString("fr-FR", options),
      });
    });

    const jsonData = JSON.stringify(data);

    await axios.post(`${config.public.backUrl}/api/affect_preference_group`, jsonData, {
      headers: {
        "Content-Type": "application/json",
      },
    });
  } catch (error) {
    console.error("Erreur lors de la création du groupe :", error);
  }
};

const validateRanking = async () => {
  await setGroupPreferencies();
  await navigateTo(
    `/rankingProjectsConfirmation/${route.params.sessionId}/${route.params.groupId}`
  );
};

onMounted( async() => {
  await getProjects();
  state.isLoading = true;
})

</script>
