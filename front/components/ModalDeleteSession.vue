<template>
  <div>
    <Modal @close="$emit('update:isOpen', false)">
      <template v-slot:open-btn>
        <div v-if="props.hideButton" class="hidden" ref="openBtn"></div>
        <div v-else class="btn btn-square">
          <img alt="delete-svg" src="../public/delete.svg" class="h-6 w-6" />
        </div>
      </template>
      <template v-slot:form>
        <div class="flex flex-col">
          <h2 class="font-semibold text-primary text-center mb-5 text-xl">
            Supprimer une session
          </h2>
          <div class="text-secondary">
            <p class="mb-2 text-center">
              Voulez-vous supprimer la session {{ sessionTitle }}?
            </p>
          </div>
        </div>
      </template>
      <template v-slot:action>
        <button class="mt-5">
          <ButtonPrimary @click="handleSubmit" title="Valider">Valider</ButtonPrimary>
        </button>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import axios from "axios";
import { useToasterStore } from '@/stores/toaster';

const toaster = useToasterStore();

const openBtn = ref(null);

const emit = defineEmits(["update:isOpen", "handleDelete"]);

const props = defineProps({
  isOpen: Boolean,
  sessionTitle: String,
  sessionId: Number,
  hideButton: Boolean,
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
  try {
    await axios.post("http://127.0.0.1:5000/api/delete_session", {
      sessionID: props.sessionId,
    });
    emit("handleDelete");
    toaster.showMessage("La session a bien été supprimée", "success");

  } catch (error) {
    emit("handleDelete");
    console.error("Erreur lors de la suppression de la session", error);
    toaster.showMessage("Erreur lors de la suppression de la session", "error");
  }
};
</script>
