<template>
    <div>
      <div>
        <h2 class="text-3xl my-8 font-extrabold text-center">{{title}}</h2>
        <h3 class="m-5 text-secondary text-center">{{ subTitle }}</h3>
      </div>
      <div class="flex justify-center">
          <Card class="h-[70vh] w-[95vw] md:w-[580px] overflow-y-scroll" no-fit>
              <Steps :nb-steps="2" :nb-steps-active="step" :nb-steps-lock="stepLock" class="w-full"></Steps>
              <div class="divider"></div> 
              <h2 class="text-xl my-4 font-bold ml-2">{{ cardTitle }}</h2>
              <h3 class="ml-2 text-secondary">{{ cardSubTitle }}</h3>
              <slot></slot>
          </Card>
      </div>
      <div class="flex justify-center">
        <div class="flex justify-center md:justify-end md:w-[580px] mt-5">
          <ButtonPrimary @click="validateGroup">{{buttonTitle}}</ButtonPrimary>
        </div>
      </div>
    </div>
  </template>
  
<script setup>
defineProps({
title: String,
subTitle: String,
step: Number,
stepLock: Number,
cardTitle: String,
cardSubTitle: String,
buttonTitle: String
});

</script>
  