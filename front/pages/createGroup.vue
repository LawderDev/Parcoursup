<template>
  <div>
    <div>
      <h2 class="text-3xl my-8 font-extrabold text-center">GROUPE</h2>
      <h3 class="m-5 text-secondary text-center">
        Renseignez les informations ci-dessous afin de créer votre demande de projet
      </h3>
    </div>
    <div class="flex justify-center">
        <Card class="h-[70vh] w-[95vw] md:w-[580px] overflow-y-scroll" no-fit>
            <Steps :nb-steps="2" :nb-steps-active="1" :nb-steps-lock="1" class="w-full"></Steps>
            <div class="divider"></div> 
            <h2 class="text-xl my-4 font-bold ml-2">Votre groupe</h2>
            <h3 class="ml-2 text-secondary">De qui est composé votre groupe ?</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div v-for="(_, index) in state.persons" class="w-fit">
                <h3 class="ml-2 mb-2 font-bold">{{ 'Personne ' + (index + 1) }}</h3>
                <AutoComplete v-model:selected="state.persons[index]"></AutoComplete>
              </div>

              <div class="mt-8">
                <ImageButton :src="ButtonPlus" class="shadow-md min-h-[2.5rem] h-[2.5rem]" @click="addPerson">Ajouter un membre</ImageButton>
              </div>
          </div>
        </Card>
    </div>
    <div class="flex justify-center">
      <div class="flex justify-center md:justify-end md:w-[580px] mt-5">
        <ButtonPrimary @click="validateGroup">Valider le groupe</ButtonPrimary>
      </div>
    </div>
  </div>
</template>

<script setup>
import ButtonPlus from "@/assets/images/plus.png"

const state = reactive({
  persons : [],
})

const addPerson = () => {
   state.persons.push({})
}

const validateGroup = async () => {
  console.log(state.persons)
  await navigateTo('/createGroupConfirmation')
}

</script>
