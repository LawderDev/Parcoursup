<template>
    <div>
      <Modal>
        <template v-slot:open-btn>
            <ButtonAdd>Ajouter un groupe</ButtonAdd> 
        </template>

        <template v-slot:form>
            <div>
                <FormCreateGroup title="Nouveau groupe" subTitle="De qui est composé votre groupe ?" v-model:group="stateCreateGroup.group" :groups="groups"></FormCreateGroup>
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

  const emit = defineEmits(["handleCreateGroup"]);

  const props = defineProps({
    groups : Array,
  });

  const handleSubmit = async() => {
    const res = await validateGroup([])
    
    nextTick(() => {
      emit('handleCreateGroup', { id : res.data.result[0], students : stateCreateGroup.group })
    })
  }
  </script>
  