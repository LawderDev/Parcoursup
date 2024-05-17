<template>
    <div>
      <div>
        <h2 class="text-3xl my-8 font-extrabold text-center">{{title}}</h2>
        <h3 class="ml-2 text-secondary text-center md:hidden">{{ subTitleMobile }}</h3>
        <h3 class="ml-2 text-secondary text-center hidden md:block">{{ subTitle }}</h3>
      </div>
      <div class="flex justify-center mt-8">
          <Card class="h-[55vh] w-[95vw] mt-6 md:w-[580px]" no-fit>
              <div class="flex justify-center items-center">
                <img src="../public/confirmation.svg" alt="confirmation" class="w-36 h-36"/>
              </div>
              <h2 class="text-xl my-4 font-bold ml-2 text-center">{{cardTitle}}</h2>
              <div class="flex gap-2 items-center mb-4 hidden md:flex ">
                <div class="flex-auto justify-start btn min-h-2 h-10 rounded-full neumorphism">
                    <span class="text-xs font-bold flex-auto text-neutral">Groupe</span>
                    <Tooltip content="element.description">...</Tooltip>
                </div>
                <img class="h-8 w-8" alt="arrow-right" src="@/public/arrow-right.svg"/>
                <div class="flex-auto justify-start btn min-h-2 h-10 rounded-full neumorphism">
                    <span class="text-xs font-bold flex-auto text-neutral">Projet 1</span>
                    <Tooltip content="element.description">?</Tooltip>
                </div>
              </div>
              <ButtonPrimary>{{ downloadButton }}</ButtonPrimary>
          </Card>
      </div>
      <div class="flex justify-center">
        <div class="flex justify-start md:w-[580px] mt-5">
          <ButtonSecondary @click="$emit('handleButtonClick')">{{buttonTitle}}</ButtonSecondary>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps({
    title: String,
    subTitleMobile: String,
    subTitle: String,
    cardTitle: String,
    downloadButton: String,
    buttonTitle: String,
    nbSteps: Number,
    nbStepsActive: Number,
    nbStepsLock: Number,
  })

  defineEmits(['handleButtonClick'])
  </script>
