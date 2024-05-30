<template>
  <div :disabled="props.disabled">
    <div @click="handleClickOpen">
      <slot name="open-btn"></slot>
    </div>

    <dialog ref="dialog" class="modal flex items-center justify-center"  @cancel="$emit('close')">
      <Toaster :message="toaster.message" :type="toaster.type" :duration="toaster.duration" :is-open="toaster.isOpen"></Toaster>
      <div
        class="modal-box max-w-fit md:w-auto md:h-auto md:rounded-xl md:drop-shadow-md"
        :class="{'w-[100vw] h-[100vh] max-h-[100vh] rounded-none': isFullOnMobile }"
      >
        <slot name="form"></slot>
        <div class="modal-action justify-center mt-0">
          <form method="dialog">
            <button
              @click="$emit('close')"
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
import { useToasterStore } from '@/stores/toaster';
import { ref } from "vue";

const dialog = ref(null);

const props = defineProps({
  isFullOnMobile: Boolean,
  disabled: Boolean,
});

defineEmits(["handleSubmit", "close"]);

const handleClickOpen = () => {
  if(!props.disabled) dialog.value.showModal();
}

const toaster = useToasterStore();
</script>
