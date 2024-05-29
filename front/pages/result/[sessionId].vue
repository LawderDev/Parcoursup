<template>
    <ProjectsConfirmation 
        v-if="state.isLoading"
        title="RESULTATS"
        sub-title-mobile="Télécharger l'assignation des projets"
        sub-title="Visualiser et télécharger l'assignation des projets"
        card-title="Les projets ont bien été assignés" 
        send-mails="Envoyer le résultat à tous les groupes"
        download-button="Télécharger le résultat"
        button-title="Retour"
        :assignations="state.assignations"
        :nb-steps="2"
        :nb-steps-active="2"
        :nb-steps-lock="0"
        @handleButtonClick="previousStep">
    </ProjectsConfirmation>
    <Skeleton v-else></Skeleton>
</template>

<script setup>
import axios from "axios";
const route = useRoute();
import { useGroups } from "../../composables/useGroups";

const state = reactive({
    assignations: [],
    isLoading: false
})

const {stateProject, api_call_projects} = useProject();
const {stateGroups, getAllGroups} = useGroups()
const config = useRuntimeConfig();

const getAssignations = async () => {
    try {
        const data = {
            sessionID: route.params.sessionId
        }
        const jsonData = JSON.stringify(data);
        const res = await axios.post(
            `${config.public.backUrl}/api/gale_shapley`,
            jsonData,
            {
                headers: {
                    "Content-Type": "application/json",
                },
            }
        );
        await api_call_projects(route.params.sessionId);
        await getAllGroups(route.params.sessionId);
        const assignations = res.data.matched_pairs.map(assignation => {
            return {
                group: stateGroups.groups.find(group => group.id === Number(assignation.man)),
                project: stateProject.projects.find(project => project.id === Number(assignation.woman))
            }
        })

        assignations.sort((a, b) => a.group.id - b.group.id);

        state.assignations = assignations.map((assignation, index) => {
            return {
                group: {
                    id: assignation.group.id,
                    nom: `Groupe ${index + 1}`,
                    students: assignation.group.students,
                    description: assignation.group.students.map(student => `${student.name} ${student.firstname}`).join(",\n ")
                },
                project: assignation.project,
            }
        })
    } catch (err) {
        console.error(err);
    }
}


const previousStep = async () => {
    await navigateTo(`/session/${route.params.sessionId}`)
}

onMounted(async () => {
    await getAssignations();
    state.isLoading = true
})
</script>