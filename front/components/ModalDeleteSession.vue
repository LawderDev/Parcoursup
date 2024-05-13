<template>
    <div>
      <Modal @handle-submit="handleSubmit" @close="$emit('update:isOpen', false)">
        <template v-slot:open-btn>
            <div class="hidden" ref="openBtn">
            </div>
        </template>
        <template v-slot:form>
          <div class="flex flex-col">
            <h2 class="font-semibold text-primary text-center mb-5 text-xl">Supprimer un projet</h2>
            <div class="text-secondary">
                <p class="mb-2 text-center">Voulez-vous supprimer ce projet ?</p>
            </div>
          </div>
        </template>
      </Modal>
    </div>
  </template> 
  
  <script setup>
  const openBtn = ref(null);

  defineEmits(["update:isOpen"])

  const props = defineProps({
    isOpen: Boolean,
  });

  watch(
    () => props.isOpen,
    () => {
      if (props.isOpen) {
        openBtn.value.click();
      }
    })

  const handleSubmit = async () => {
    /*try {
      await axios.post("http://127.0.0.1:5000/api/delete-session");
    } catch (error) {
      console.error("Error delete session:", error);
    }*/
  };
  </script>
  