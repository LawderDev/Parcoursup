<template>
  <div>
    <NavBar :nom="'fdsf'" />
    <div class="m-8 mx-10">
      <h1 class="text-3xl my-8 font-bold">Projet TIC 2024</h1>
      <input
        type="file"
        class="file-input file-input-primary file-input-bordered file-input-sm w-full max-w-xs rounded-badge"
      />
      <h2 class="text-xl my-8 font-semibold">Nombre de personnes par groupe</h2>
      <label
        class="input input-bordered flex items-center gap-4 m-4 rounded-badge"
      >
        Minimum
        <input type="number" class="grow" placeholder="Entrez un nombre" />
      </label>
      <label
        class="input input-bordered flex items-center gap-4 m-4 rounded-badge"
      >
        Maximum
        <input type="number" class="grow" placeholder="Entrez un nombre" />
      </label>
      <h2 class="text-xl my-8 font-semibold">Date de fin</h2>
      <Date class="px-5" />
      <h2 class="text-xl mt-8 mb-4 font-semibold">Projets</h2>
      <h3 class=" ml-5 text-gray-500">Quels seront les projets disponibles ?</h3>
    </div>
  </div>
</template>
<script setup>
import Date from "~/components/Date.vue";
import NavBar from "~/components/NavBar.vue";
</script>
