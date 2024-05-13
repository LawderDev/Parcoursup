<template>
  <div>
    <Modal @handle-submit="handleSubmit">
      <template v-slot:open-btn>
        <ButtonPrimary> Créer une session </ButtonPrimary>
      </template>
      <template v-slot:form>
        <FormSession></FormSession>
      </template>
    </Modal>
  </div>
</template>
<script setup>

</script>
