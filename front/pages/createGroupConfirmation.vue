<template>
    <div>
      <div>
        <h2 class="text-3xl my-8 font-extrabold text-center">MERCI</h2>
      </div>
      <div class="flex justify-center">
          <Card class="h-[70vh] w-[95vw] md:w-[580px] overflow-y-scroll" no-fit>
              <Steps :nb-steps="2" :nb-steps-active="1" :nb-steps-lock="1" class="w-full"></Steps>
              <div class="divider"></div> 
              <div class="flex justify-center items-center">
                <img src="../public/confirmation.svg" alt="confirmation" class="w-36 h-36"/>
              </div>
              <h2 class="text-xl my-4 font-bold ml-2 text-center">Votre groupe à bien été créé</h2>
              <h3 class="ml-2 text-secondary text-center">Vous recevrez bientot plus d’informations. Restez en contact avec votre professeur référent.</h3>
          </Card>
      </div>
      <div class="flex justify-center">
        <div class="flex justify-start md:w-[580px] mt-5">
          <ButtonSecondary @click="previousStep">Etape précédente</ButtonSecondary>
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
  
  const previousStep = async () => {
    await navigateTo('/createGroup')
  }
  
  </script>
  