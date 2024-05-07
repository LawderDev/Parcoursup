<template>
    <div>
      <Modal @handle-submit="handleSubmit">
        <template v-slot:open-btn>
            <div class="btn btn-square">
                <img alt="delete-svg" src="../public/delete.svg" class="h-6 w-6" />
            </div>
        </template>
        <template v-slot:form>
          <div class="flex flex-col">
            <h2 class="font-semibold text-primary text-center mb-5 text-xl">Supprimer un projet</h2>
            <div class="text-secondary">
                <p class="mb-2">Voulez-vous supprimer ce projet ?</p>
            </div>
          </div>
        </template>
      </Modal>
    </div>
  </template> 
  
  <script setup>
  const handleSubmit = () => {
  
  };
  </script>
  