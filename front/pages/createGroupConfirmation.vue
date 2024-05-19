<template>
        <StudentsConfirmation 
            title="MERCI" 
            cardTitle="Votre groupe a bien été créé" 
            cardSubTitle="Vous recevrez bientot plus d’informations. Restez en contact avec votre professeur référent."
            :nb-steps="2"
            :nb-steps-active="1"
            :nb-steps-lock="1"
            @handleButtonClick="previousStep">
        </StudentsConfirmation>
  </template>
  
  <script setup>
  const previousStep = async () => {
    await navigateTo('/createGroup')
  }
  
  </script>
  