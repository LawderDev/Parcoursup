<template>
  <StudentsActions 
    title="GROUPE"
    :nb-steps="2"
    :nb-steps-active="1"
    :nb-steps-lock="1"
    sub-title="Renseignez les informations ci-dessous afin de créer votre demande de projet"
    button-title="Valider le groupe"
    @handle-button-click="handleValidateGroup">
      <FormCreateGroup title="Votre groupe" subTitle="De qui est composé votre groupe ?" v-model:group="stateCreateGroup.group" :groups="state.groups"></FormCreateGroup>
  </StudentsActions>
</template>

<script setup>
const {stateCreateGroup, validateGroup} = useCreateGroup()

const state = reactive({
  groups: [],
})

const getAllGroups = async () => {
    try {
      const data = {
        sessionID: route.params.sessionId
      }

      const jsonData = JSON.stringify(data);

      const res = await axios.post(
        "http://127.0.0.1:5000/api/get_all_groups_students",
        jsonData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      
      state.groups = res.data
    } catch (err) {
      console.error(err);
    }
  }

const handleValidateGroup = async () => {
  await validateGroup()
  await navigateTo('/createGroupConfirmation')
}
</script>
