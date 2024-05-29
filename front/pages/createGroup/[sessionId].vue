<template>
  <StudentsActions 
    v-if="state.isLoading"
    title="GROUPE"
    :nb-steps="2"
    :nb-steps-active="1"
    :nb-steps-lock="1"
    :button-disabled="!canValidateGroup()"
    sub-title="Renseignez les informations ci-dessous afin de créer votre demande de projet"
    button-title="Valider le groupe"
    @handle-button-click="handleValidateGroup">
      <FormCreateGroup title="Votre groupe" subTitle="De qui est composé votre groupe ?" v-model:group="stateCreateGroup.group" :groups="stateGroups.groups" :groupMin="stateSession.session.group_min" :groupMax="stateSession.session.group_max"></FormCreateGroup>
  </StudentsActions>
  <Skeleton v-else></Skeleton>
</template>

<script setup>
import axios from "axios";
import { useGroups} from "~/composables/useGroups";
import { useSessionData } from "~/composables/useSessionData";
const { stateCreateGroup, validateGroup } = useCreateGroup()
const { stateGroups, getAllGroups } = useGroups()
const { stateSession, getSessionData } = useSessionData()

const route = useRoute()

const state = reactive({
  isLoading: false,
});

const canValidateGroup = () => {
  return stateCreateGroup.group.length >= stateSession.session.group_min && stateCreateGroup.group.length <= stateSession.session.group_max;
}

definePageMeta({
  middleware: ['check-end-date-group'] // Pass parameters here
})

const handleValidateGroup = async () => {
  await validateGroup(stateCreateGroup.group)
  await navigateTo('/createGroupConfirmation')
}

onMounted(async () => {
  await getAllGroups(route.params.sessionId);
  await getSessionData(route.params.sessionId);
  state.isLoading = true;
})

</script>
