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
import axios from "axios";
const route = useRoute();

const state = reactive({
    assignations: [],
})

const getAssignations = async () => {
    try {
        /**data = {
            "men_preferences": {
                "man1": ["woman1", "woman2", "woman3"],
            },
            "women_preferences": {
                "woman1": ["man1", "man2", "man3"],
            }
        }*/


        const data = {
            sessionID: route.params.sessionId
        }
        const jsonData = JSON.stringify(data);
        const res = await axios.post(
            "http://127.0.0.1:5000/api/gale_shapley",
            jsonData,
            {
                headers: {
                    "Content-Type": "application/json",
                },
            }
        );
        console.log(res.data)
        //state.assignations = res.data
    } catch (err) {
        console.error(err);
    }
}


const previousStep = async () => {
    await navigateTo(`/session/${route.params.sessionId}`)
}

await getAssignations();
</script>