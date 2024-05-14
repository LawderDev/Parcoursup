<template>
    <StudentsConfirmation 
        title="MERCI" 
        cardTitle="Vos préférences ont bien été prises en compte" 
        cardSubTitle="Vous recevrez bientot plus d’informations. Restez en contact avec votre professeur référent."
        buttonTitle="Etape précédente" 
        :nb-step="2"
        :nb-step-active="2"
        :nb-step-lock="0"
        @handleButtonClick="previousStep">
    </StudentsConfirmation>
</template>

<script setup>
const previousStep = async () => {
    await navigateTo('/rankingProjects')
}

</script>
