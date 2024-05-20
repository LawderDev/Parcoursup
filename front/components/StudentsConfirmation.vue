<template>
    <div>
      <div>
        <h2 class="text-3xl my-8 font-extrabold text-center">{{title}}</h2>
      </div>
      <div class="flex justify-center">
          <Card class="h-[70vh] w-[95vw] md:w-[580px] overflow-y-scroll" no-fit>
              <Steps :nb-steps="nbSteps" :nb-steps-active="nbStepsActive" :nb-steps-lock="nbStepsLock" class="w-full"></Steps>
              <div class="divider"></div> 
              <div class="flex justify-center items-center">
                <img src="../public/confirmation.svg" alt="confirmation" class="w-36 h-36"/>
              </div>
              <h2 class="text-xl my-4 font-bold ml-2 text-center">{{cardTitle}}</h2>
              <h3 class="ml-2 text-secondary text-center">{{ cardSubTitle }}</h3>
          </Card>
      </div>
      <div class="flex justify-center">
        <div class="flex justify-start md:w-[580px] mt-5">
          <ButtonSecondary v-if="buttonTitle" @click="$emit('handleButtonClick')">{{buttonTitle}}</ButtonSecondary>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps({
    title: String,
    cardTitle: String,
    cardSubTitle: String,
    buttonTitle: String,
    nbSteps: Number,
    nbStepsActive: Number,
    nbStepsLock: Number,
  })

  defineEmits(['handleButtonClick'])
  </script>
