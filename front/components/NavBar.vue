<template>
  <div>
    <div
      class="flex justify-between items-center navbar-center bg-base-100 shadow-lg rounded-badge m-4 p-5 px-8"
    >
      <div>
        <div class="avatar">
          <div class="w-16 rounded-xl">
            <button @click="redirectToIndex">
              <img src="../public/logo.png" alt="logo" />
            </button>
          </div>
        </div>
      </div>
      <div>
        <button @click="redirectToIndex">
          <h1 class="text-xl md:block">Smart Choice</h1>
        </button>
      </div>
      <div class="dropdown dropdown-end">
        <div tabindex="0" role="button" class="btn btn-ghost btn-circle">
          <div class="avatar placeholder">
            <div class="bg-primary text-neutral-content rounded-full w-12">
              <span v-if="letter" class="text-xl uppercase">{{ letter }}</span>
            </div>
          </div>
        </div>
        <ul
          tabindex="0"
          class="shadow menu menu-sm dropdown-content bg-base-100 rounded-box w-40 md:w-60"
        >
          <li class="pl-1">
            <ModalProfile> </ModalProfile>
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
const props = defineProps(["name"]);
const letter = computed(() => props.name.charAt(0));

const redirectToIndex = async () => {
  await navigateTo(`/`);
};
</script>
