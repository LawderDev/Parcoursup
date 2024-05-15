<template>
  <div>
    <Modal @handle-submit="handleSubmit">
      <template v-slot:open-btn>
        <ButtonPrimary> Créer une session </ButtonPrimary>
      </template>
      <template v-slot:form>
        <h1 class="font-semibold text-primary text-center mb-5 p-4 text-xl">
          Créer une session
        </h1>
        <FormSession></FormSession>
      </template>
    </Modal>
  </div>
</template>
<script setup></script>
