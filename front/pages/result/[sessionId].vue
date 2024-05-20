<template>
    <ProjectsConfirmation 
        title="RESULTATS"
        subTitleMobile="Télécharger l'assignation des projets"
        subTitle="Visualiser et télécharger l'assignation des projets"
        cardTitle="Les projets ont bien été assignés" 
        downloadButton="Télécharger le résultat"
        buttonTitle="Retour"
        :assignations="state.assignations"
        :nb-steps="2"
        :nb-steps-active="2"
        :nb-steps-lock="0"
        @handleButtonClick="previousStep">
    </ProjectsConfirmation>
</template>

<script setup>
import axios from "axios";
const route = useRoute();
import { useGroups } from "../../composables/useGroups";

const state = reactive({
    assignations: [],
})

const {stateProject, api_call_projects} = useProject();
const {stateGroups, getAllGroups} = useGroups()

const getAssignations = async () => {
    try {
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
        await api_call_projects(route.params.sessionId);
        console.log(stateProject.projects);
        await getAllGroups(route.params.sessionId);
        console.log(stateGroups.groups);
        const assignations = res.data.matched_pairs.map(assignation => {
            return {
                group: stateGroups.groups.find(group => group.id === Number(assignation.man)),
                project: stateProject.projects.find(project => project.id === Number(assignation.woman))
            }
        })
        console.log(state.assignations)

        assignations.sort((a, b) => a.group.id - b.group.id);

        state.assignations = assignations.map((assignation, index) => {
            return {
                group: {
                    id: assignation.group.id,
                    nom: `Groupe ${index + 1}`,
                    description: assignation.group.students.map(student => `${student.name} ${student.firstname}`).join(",\n ")
                },
                project: assignation.project,
            }
        })

        console.log(state.assignations)
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