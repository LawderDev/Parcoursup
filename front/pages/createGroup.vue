<template>
  <StudentsActions 
    title="GROUPE"
    :nb-steps="2"
    :nb-steps-active="1"
    :nb-steps-lock="1"
    sub-title="Renseignez les informations ci-dessous afin de créer votre demande de projet"
    button-title="Valider le groupe"
    @handle-button-click="validateGroup">
      <h1 class="card-title pb-4 text-neutral">Votre groupe</h1>
      <h2 class="pb-4 text-accent text-sm">De qui est composé votre groupe ?</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div v-for="(_, index) in state.persons" class="w-fit">
            <h3 class="ml-2 mb-2 font-bold">{{ 'Personne ' + (index + 1) }}</h3>
            <AutoComplete v-model:selected="state.persons[index]" :peoples="peoples" :default-index="0"></AutoComplete>
        </div>

        <div class="mt-8">
          <ImageButton :src="ButtonPlus" class="shadow-md min-h-[2.5rem] h-[2.5rem]" @click="addPerson">Ajouter un membre</ImageButton>
        </div>
      </div>
  </StudentsActions>
</template>

<script setup>
import ButtonPlus from "@/assets/images/plus.png"

const state = reactive({
  persons : [],
})

const peoples = [
    { id: 1, firstname:'Wade', name:"Cooper", email: "wade.cooper@example.com" },
    { id: 2, firstname: 'Arlene', name:"Mccoy", email: "arlene.mccoy@example.com" },
    { id: 3, firstname: 'Devon', name: 'Webb', email: "devon.webb@example.com" },
    { id: 4, firstname:'Tom', name: 'Cook', email: "tom.cook@example.com" },
    { id: 5, firstname: 'Tanya', name: 'Fox', email: "tanya.fox@example.com" },
    { id: 6, firstname:'Hellen', name: 'Schmidt', email: "hellen.schmidt@example.com" },
];

const addPerson = () => {
   state.persons.push({})
}

const validateGroup = async () => {
  console.log(state.persons)
  await navigateTo('/createGroupConfirmation')
}

</script>
