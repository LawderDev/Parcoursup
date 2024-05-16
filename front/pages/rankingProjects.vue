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
  const state = reactive({
    projects : [{
      name: "Projet 1",
      description: "LOREM IPSUM LOREM IPSUM LOREM IPSUM V VLOREM IPSUMLOREM IPSUMLOREM IPSUMLOREM IPSUMLOREM IPSUMLOREM IPSUMLOREM IPSUMLOREM IPSUMLOREM IPSUMLOREM IPSUMLOREM IPSUMLOREM IPSUM"
    },
    {
      name: "Projet 2",
      description: "test"
    },
    {
      name: "Projet 3",
      description: "test"
    },
    {
      name: "Projet 4",
      description: "test"
    }],
  })
  
  
  const validateRanking = async () => {
    console.log(state.projects)
    await navigateTo('/rankingProjectsConfirmation')
  }
  
  </script>
  