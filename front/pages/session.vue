<template>
  <div>
    <NavBar :name="'fdsf'" />
    <form class="grid m-8 mx-10" method="post">
      <h1 class="text-3xl my-8 font-bold">Projet TIC 2024</h1>
      <FileInput />
      <h2 class="text-xl my-8 font-semibold">Nombre de personnes par groupe</h2>
      <div class="">
        <label
          class="input input-bordered flex items-center gap-4 m-4 rounded-badge"
        >
          Minimum
          <input
            v-model="state.minGroup"
            type="number"
            class="grow"
            placeholder="Entrez un nombre"
            :min="0"
            :max="state.maxGroup"
          />
        </label>
        <label
          class="input input-bordered flex items-center gap-4 m-4 rounded-badge"
        >
          Maximum
          <input
            v-model="state.maxGroup"
            type="number"
            class="grow"
            placeholder="Entrez un nombre"
            :min="state.minGroup"
            :max="9999"
          />
        </label>
      </div>
      <h2 class="text-xl my-8 font-semibold">Date de fin</h2>
      <Date class="px-5" />
      <h2 class="text-xl mt-8 mb-4 font-semibold">Projets</h2>
      <h3 class="ml-5 text-gray-500">Quels seront les projets disponibles ?</h3>
      <ProjectCard class="m-5" title="Card 1" :summary="'lorem ipsum dolor sit amet, consectetur'"/>
      <ButtonPrimary class="md:place-self-end">Enregistrer les modifications</ButtonPrimary>
    </form>
  </div>
</template>

<script setup>
import Date from "~/components/Date.vue";
import NavBar from "~/components/NavBar.vue";
import FileInput from "~/components/FileInput.vue";
import ButtonPrimary from "~/components/ButtonPrimary.vue";
import ProjectCard from "~/components/ProjectCard.vue"
const state = reactive({
  minGroup: 1,
  maxGroup: null,
});

</script>
