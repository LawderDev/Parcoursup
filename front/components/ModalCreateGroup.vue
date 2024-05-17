<template>
    <div>
      <Modal @close="$emit('update:isOpen', false)">
        <template v-slot:open-btn>
            <ButtonAdd ref="openBtn">Ajouter un groupe</ButtonAdd> 
        </template>

        <template v-slot:form>
            <div>
                <FormCreateGroup title="Nouveau groupe" subTitle="De qui est composé votre groupe ?" v-model:group="stateCreateGroup.group"></FormCreateGroup>
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
  const {stateCreateGroup, validateGroup} = useCreateGroup()

  const openBtn = ref(null);

  const emit = defineEmits(["update:isOpen", "handleCreateGroup"]);

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

  const handleSubmit = async() => {
    await validateGroup()
    nextTick(() => {
      emit('handleCreateGroup')
    })
  }
  </script>
  