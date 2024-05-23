<template>
  <div>
    <div class="flex justify-center my-10 mb-12">
      <span class="loading loading-spinner loading-lg text-accent"></span>
    </div>
    <div class="flex flex-col gap-5 my-8  ">
      <div class="flex gap-5 items-center">
        <div class="skeleton w-16  h-16 rounded-full"></div>
        <div class="flex flex-col gap-4 md:w-[40vw]">
          <div class="skeleton h-4 w-28 md:w-[70%]"></div>
          <div class="skeleton h-4 w-36 md:w-full"></div>
        </div>
      </div>
    </div>
    <div class="flex flex-col gap-5">
      <div class="skeleton h-32 text-secondary"></div>
      <div class="skeleton h-4"></div>
      <div class="skeleton h-4"></div>
      <div class="skeleton h-4"></div>
    </div>
  </div>
</template>
