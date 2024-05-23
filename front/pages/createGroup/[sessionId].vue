<template>
  <StudentsActions 
    title="GROUPE"
    :nb-steps="2"
    :nb-steps-active="1"
    :nb-steps-lock="1"
    sub-title="Renseignez les informations ci-dessous afin de créer votre demande de projet"
    button-title="Valider le groupe"
    @handle-button-click="handleValidateGroup">
      <FormCreateGroup title="Votre groupe" subTitle="De qui est composé votre groupe ?" v-model:group="stateCreateGroup.group" :groups="stateGroups.groups" :groupMin="stateSession.session.group_min" :groupMax="stateSession.session.group_max"></FormCreateGroup>
  </StudentsActions>
</template>

<script setup>
import axios from "axios";
import { useGroups} from "~/composables/useGroups";
import { useSessionData } from "~/composables/useSessionData";
const { stateCreateGroup, validateGroup } = useCreateGroup()
const { stateGroups, getAllGroups } = useGroups()
const { stateSession, getSessionData } = useSessionData()


const route = useRoute()

const handleValidateGroup = async () => {
  await validateGroup(stateCreateGroup.group)
  await navigateTo('/createGroupConfirmation')
}

await getAllGroups(route.params.sessionId);
await getSessionData(route.params.sessionId);
</script>
