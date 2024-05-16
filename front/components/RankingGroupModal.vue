<template>
   <Modal>
        <template v-slot:open-btn>
            <ButtonPrimary>Vos préférences</ButtonPrimary>
        </template>
        <template v-slot:form>
            <h2 class="font-semibold text-primary text-center mb-5 text-xl">Supprimer une session</h2>
          
            <Ranking :items="state.groups" description="Classez les groupes de projets en fonction de vos préférences"></Ranking>
        </template>
        <template v-slot:action>
            <button class="mt-5">
              <ButtonPrimary @click="handleSubmit" title="Valider">Valider</ButtonPrimary>
          </button>
        </template>
   </Modal>
  </template>


  <script setup>
    const state = reactive({
        groups : [{
        name: "Groupe 1",
        description: "LOREM IPSUM LOREM IPSUM LOREM IPSUM V VLOREM IPSUMLOREM IPSUMLOREM IPSUMLOREM IPSUMLOREM IPSUMLOREM IPSUMLOREM IPSUMLOREM IPSUMLOREM IPSUMLOREM IPSUMLOREM IPSUMLOREM IPSUM"},
        {
        name: "Groupe 2",
        description: "test"
        },
        {
        name: "Groupe 3",
        description: "test"
        },
        {
        name: "Groupe 4",
        description: "test"
    }],
  })

  const handleSubmit = async () => {
    console.log(state.groups)
  }
  </script>
  