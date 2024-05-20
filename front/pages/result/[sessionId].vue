<template>
    <ProjectsConfirmation 
        title="RESULTATS"
        subTitleMobile="Télécharger l'assignation des projets"
        subTitle="Visualiser et télécharger l'assignation des projets"
        cardTitle="Les projets ont bien été assignés" 
        downloadButton="Télécharger le résultat"
        buttonTitle="Retour" 
        :nb-steps="2"
        :nb-steps-active="2"
        :nb-steps-lock="0"
        @handleButtonClick="previousStep">
    </ProjectsConfirmation>
</template>

<script setup>
const route = useRoute();

const previousStep = async () => {
    await navigateTo(`/session/${route.params.sessionId}`)
}

</script>