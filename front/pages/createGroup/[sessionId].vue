<template>
  <StudentsActions 
    title="GROUPE"
    :nb-steps="2"
    :nb-steps-active="1"
    :nb-steps-lock="1"
    sub-title="Renseignez les informations ci-dessous afin de créer votre demande de projet"
    button-title="Valider le groupe"
    @handle-button-click="handleValidateGroup">
      <FormCreateGroup title="Votre groupe" subTitle="De qui est composé votre groupe ?" v-model:group="stateCreateGroup.group" :groups="stateGroups.groups"></FormCreateGroup>
  </StudentsActions>
</template>

<script setup>
import axios from "axios";
import {useGroups} from "~/composables/useGroups";
const {stateCreateGroup, validateGroup} = useCreateGroup()
const {stateGroups, getAllGroups} = useGroups()

const route = useRoute()

definePageMeta({
  middleware: ['check-end-date-group'] // Pass parameters here
})

const handleValidateGroup = async () => {
  console.log(stateCreateGroup.group)
  await validateGroup(stateCreateGroup.group)
  await navigateTo('/createGroupConfirmation')
}

await getAllGroups(route.params.sessionId);
</script>
