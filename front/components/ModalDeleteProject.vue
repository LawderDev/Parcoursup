<template>
    <div>
      <Modal @close="$emit('update:isOpen', false)">
        <template v-slot:open-btn>
            <div class="hidden" ref="openBtn">
            </div>
        </template>
        <template v-slot:form>
          <div class="flex flex-col">
            <h2 class="font-semibold text-primary text-center mb-5 text-xl">Supprimer une session</h2>
            <div class="text-secondary">
                <p class="mb-2 text-center">Voulez-vous supprimer la session {{ sessionTitle }}?</p>
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
  const openBtn = ref(null);

  defineEmits(["update:isOpen"])

  const props = defineProps({
    isOpen: Boolean,
    sessionTitle: String,
    sessionId: Number,
  });

  watch(
    () => props.isOpen,
    () => {
      if (props.isOpen) {
        openBtn.value.click();
      }
    })

  const handleSubmit = async () => {
    //TODO use sessionId parameter to delete
    /*try {
      await axios.post("http://127.0.0.1:5000/api/delete-session");
    } catch (error) {
      console.error("Error delete session:", error);
    }*/
  };
  </script>
  