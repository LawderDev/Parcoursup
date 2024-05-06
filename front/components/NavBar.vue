<template>
  <div>
    <div
      class="flex justify-between items-center navbar-center bg-base-100 shadow-lg rounded-badge m-4 p-5 px-8"
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
      <div class="dropdown dropdown-end">
        <div tabindex="0" role="button" class="btn btn-ghost btn-circle">
          <div class="avatar placeholder">
            <div class="bg-primary text-neutral-content rounded-full w-12">
              <span v-if="lettre" class="text-xl uppercase">{{ lettre }}</span>
            </div>
          </div>
        </div>
        <ul
          tabindex="0"
          class="shadow menu menu-sm dropdown-content bg-base-100 rounded-box w-40 md:w-60"
        >
          <li class="pl-1">
            <div class="flex items-center">
              <img src="../public/settings.svg" class="w-5" />
              <a  class="md:text-lg">Profil</a>
            </div>
          </li>
          <li class="pl-1">
            <div class="flex items-center">
              <img src="../public/logout.svg" class="w-5" />
              <a class="md:text-lg">Deconnexion</a>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
<script setup>
const props = defineProps(["nom"]);
const lettre = computed(() => props.nom.charAt(0));
</script>
