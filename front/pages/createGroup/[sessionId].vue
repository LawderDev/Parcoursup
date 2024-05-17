<template>
  <StudentsActions 
    title="GROUPE"
    :nb-steps="2"
    :nb-steps-active="1"
    :nb-steps-lock="1"
    sub-title="Renseignez les informations ci-dessous afin de créer votre demande de projet"
    button-title="Valider le groupe"
    @handle-button-click="validateGroup">
      <FormCreateGroup title="Votre groupe" subTitle="De qui est composé votre groupe ?"></FormCreateGroup>
  </StudentsActions>
</template>

<script setup>

</script>
