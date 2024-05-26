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
  import { useToasterStore } from '@/stores/toaster';

  const emit = defineEmits(["handleCreateGroup"]);
  const toaster = useToasterStore();

  const props = defineProps({
    groups : Array,
  });

  const handleSubmit = async() => {
    if(!stateCreateGroup.group.length) {
      toaster.showMessage('Le groupe doit contenir au moins un membre', 'error')
      return
    }
    
    nextTick(() => {
      emit('handleCreateGroup', { id : null, students : stateCreateGroup.group })
    })
  }
  </script>
  