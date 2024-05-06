<template>
  <div>
    <NavBar :nom="'fdsf'" />
    <div class="m-8">
      <h1 class="text-3xl my-8 font-bold">Projet TIC 2024</h1>
      <input
        type="file"
        class="file-input file-input-primary file-input-bordered file-input-sm w-full max-w-xs rounded-badge"
      />
      <p class="text-xl my-8">Nombre de personnes par groupe</p>
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
      <p class="text-xl my-8">Date de fin</p>
      <Date class="px-10" />
    </div>
  </div>
</template>
<script setup>
import Date from "~/components/Date.vue";
import NavBar from "~/components/NavBar.vue";
</script>
