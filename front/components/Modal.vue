<template>
  <div>
    <div @click="dialog.showModal">
      <slot name="open-btn"></slot>
    </div>
  
    <dialog ref="dialog" class="modal "> 
      <div class="modal-box w-[100vw] h-[100vh] max-h-[100vh] rounded-none md:w-[50%] md:h-auto md:rounded-xl md:drop-shadow-md">
        
        <div class="modal-action justify-center mt-0">
          <slot name="form"></slot>
          
        </div>
      </div>
    </dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const dialog = ref(null)


</script>
