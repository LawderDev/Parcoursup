<template>
    <StudentsConfirmation 
        title="MERCI" 
        cardTitle="Vos préférences ont bien été prises en compte" 
        cardSubTitle="Vous recevrez bientot plus d’informations. Restez en contact avec votre professeur référent."
        buttonTitle="Etape précédente" 
        :nb-steps="2"
        :nb-steps-active="2"
        :nb-steps-lock="0"
        @handleButtonClick="previousStep">
    </StudentsConfirmation>
</template>

<script setup>
const route = useRoute()
const previousStep = async () => {
    await navigateTo(`/rankingProjects/${route.params.sessionId}/${route.params.groupId}`)
}

</script>
