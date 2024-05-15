<template>
  <div>
    <div @click="dialog.showModal">
      <slot name="open-btn"></slot>
    </div>

    <dialog ref="dialog" class="modal">
      <div
        class="modal-box md:w-[50%] md:h-auto md:rounded-xl md:drop-shadow-md overflow-visible"
        :class="{'w-[100vw] h-[100vh] max-h-[100vh] rounded-none': isFullOnMobile }"
      >
        <slot name="form"></slot>
        <div class="modal-action justify-center mt-0">
          <form method="dialog">
            <button
              class="btn btn-sm btn-circle btn-ghost absolute left-2 top-2"
            >
              ✕
            </button>
            <slot name="action"></slot>
          </form>
        </div>
      </div>
    </dialog>
  </div>
</template>

<script setup>
import { ref } from "vue";

const dialog = ref(null);

const props = defineProps({
    isFullOnMobile: Boolean
  });

defineEmits(["handleSubmit", "close"])
</script>
