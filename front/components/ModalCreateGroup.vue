<template>
    <div>
      <Modal @close="$emit('update:isOpen', false)">
        <template v-slot:open-btn>
            <ButtonAdd ref="openBtn">Ajouter un groupe</ButtonAdd> 
        </template>

        <template v-slot:form>
            <div>
                <FormCreateGroup title="Nouveau groupe" subTitle="De qui est composé votre groupe ?"></FormCreateGroup>
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
  