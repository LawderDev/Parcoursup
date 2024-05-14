<template>
  <div>
    <Modal @handle-submit="handleSubmit">
      <template v-slot:open-btn>
        <ButtonPrimary> Créer un projet </ButtonPrimary>
      </template>
      <template v-slot:form>
        <div class="flex flex-col items-center">
          <h1 class="text-3xl mt-3">{{ state.sessionName }}</h1>
          <div class="my-5">
            <h2 class="mx-5 my-2">Nom du projet</h2>
            <input
              type="text"
              placeholder="Type here"
              class="input input-bordered w-full max-w-xs"
            />
            <h2 class="mx-5 my-2">Description</h2>
            <input
              type="text"
              placeholder="Type here"
              class="input input-bordered w-full max-w-xs"
            />
          </div>
          <ButtonPrimary class="place-self-center">Valider</ButtonPrimary>
        </div>
      </template>
    </Modal>
  </div>
</template>
<script setup>
import Cancel from "~/public/cancel.svg";
const state = reactive({
  sessionName: "Parcoursup",
});
</script>
