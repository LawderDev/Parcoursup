<template>
  <div>
    <button class="btn" @click="dialog.showModal()">open modal</button>
    <dialog ref="dialog" class="modal">
      <div class="modal-box">
        <slot></slot>
        <div class="modal-action">
          <form method="dialog">
            <button class="btn m-5">Valider</button>
            <button class="btn">Annuler</button>
          </form>
        </div>
      </div>
    </dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const dialog = ref(null)

</script>
