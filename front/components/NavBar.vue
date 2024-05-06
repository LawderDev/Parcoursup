<template>
  <div>
    <div
      class="flex justify-between navbar-center bg-base-100 shadow-lg rounded-badge m-4 p-5 px-8"
    >
      <div>
        <div class="avatar">
          <div class="w-8 rounded">
            <img
              src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.jpg"
              alt="Tailwind-CSS-Avatar-component"
            />
          </div>
        </div>
      </div>
      <div>
        <h1 class="text-xl md:block">Nom du site</h1>
      </div>
      <div class="place-self-end">
        <div class="w-9">
          <profil :nom=props.nom />
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import profil from "./Profil.vue"
const props = defineProps(['nom'])
</script>
