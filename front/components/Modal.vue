<template>
  <div>
    <div @click="dialog.showModal">
      <slot name="open-btn"></slot>
    </div>

    <dialog ref="dialog" class="modal">
      <div
        class="modal-box w-[100vw] h-[100vh] max-h-[100vh] rounded-none md:w-[50%] md:h-auto md:rounded-xl md:drop-shadow-md"
      >
        <slot name="form"></slot>
        <div class="modal-action justify-center mt-0">
          <form method="dialog">
            <button
              class="btn btn-sm btn-circle btn-ghost absolute left-2 top-2"
            >
              ✕
            </button>
            <button class="flex justify-center mt-5">
              <ButtonPrimary @click="$emit('handleSubmit')" title="Valider">Valider</ButtonPrimary>
            </button>
          </form>
        </div>
      </div>
    </dialog>
  </div>
</template>

<script setup>
import { ref } from "vue";

const dialog = ref(null);

defineEmits(["handleSubmit"])
</script>
