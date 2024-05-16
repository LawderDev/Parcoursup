<template>
  <div>
    <Modal >
      <template v-slot:open-btn>
        <ButtonPrimary> Créer une session </ButtonPrimary>
      </template>
      <template v-slot:form>
        <h1 class="font-semibold text-primary text-center mb-5 p-4 text-xl">
          Créer une session
        </h1>
        <FormSession @handle-validate="closeModal"></FormSession>
      </template>
      <template v-slot:action>
        <button class="hidden" ref="closeBtn"></button>
      </template>
    </Modal>
  </div>
</template>
<script setup>
const closeBtn = ref(null);

const closeModal = () => {
  closeBtn.value.click();
}
</script>
