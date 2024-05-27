<template>
  <div>
    <Modal @close="$emit('update:isOpen', false)" :disabled="props.disabled">
      
      <template v-slot:open-btn>
        <button
          v-if="props.disabled"
          class="btn btn-ghost"
          disabled
        >
          <img alt="delete-svg" src="../public/delete.svg" class="h-6 w-6" />
        </button>
        <button
          v-else
          @click.stop="$emit('update:isOpen', true)"
          class="btn btn-ghost"
        >
          <img alt="delete-svg" src="../public/delete.svg" class="h-6 w-6" />
        </button>
        <div ref="openBtn" class="hidden"></div>
      </template>
      
      <template v-slot:form>
        <div class="flex flex-col">
          <h2 class="font-semibold text-primary text-center mb-5 text-xl">
            Supprimer un projet
          </h2>
          <div class="text-secondary">
            <p class="mb-2 text-center">
              Voulez-vous supprimer le projet {{ props.projectName }}?
            </p>
          </div>
        </div>
      </template>
      <template v-slot:action>
        <button @click="emit('update:isOpen', false)" class="mt-5">
          <ButtonPrimary @click="handleSubmit" title="Valider"
            >Valider</ButtonPrimary
          >
        </button>
      </template>
    </Modal>
  </div>
</template>

<script setup>
const openBtn = ref(null);

const emit = defineEmits(["deleteProject", "update:isOpen"]);

const props = defineProps({
  isOpen: Boolean,
  projectName: String,
  projectId: Number,
  disabled: Boolean,
});

watch(
  () => props.isOpen,
  () => {
    if (props.isOpen) {
      openBtn.value.click();
    }
  }
);

const handleSubmit = async () => {
  emit("deleteProject", props.projectId);
};
</script>
