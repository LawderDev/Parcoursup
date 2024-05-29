<template>
    <div>
      <Modal>
        <template v-slot:open-btn>
          <ButtonPrimary>Ajouter un utilisateur</ButtonPrimary>
        </template>
        <template v-slot:form>
            <div class="w-[75vw] md:w-[35vw]">
                <h1 class="font-semibold text-primary text-center p-4 text-xl">
                    Ajouter un utilisateur
                </h1>
                <div>
                    <h2 class="mb-2">Nom</h2>
                    <div class="flex w-full mb-5">
                        <input class="input input-bordered w-full rounded-badge"/>
                    </div>
                </div>
                <div>
                    <h2 class="mb-2">Prénom</h2>
                    <div class="flex w-full mb-5">
                        <input class="input input-bordered w-full rounded-badge"/>
                    </div>
                </div>
                <div>
                    <h2 class="mb-2">Email</h2>
                    <div class="flex w-full mb-5">
                        <input class="input input-bordered w-full rounded-badge"/>
                    </div>
                </div>
                <div>
                    <h2 class="mb-2">Mot de passe</h2>
                    <div class="flex w-full mb-5">
                        <input class="input input-bordered w-full rounded-badge"/>
                    </div>
                </div>
                <div>
                    <h2 class="mb-2">Confirmer le mot de passe</h2>
                    <div class="flex w-full mb-5">
                        <input class="input input-bordered w-full rounded-badge"/>
                    </div>
                </div>
            </div>
        </template>
        <template v-slot:action>
            <ButtonPrimary @click="handleSubmit" title="Valider">Valider</ButtonPrimary>
        </template>
      </Modal>
    </div>
</template>
<script setup>
import Connexion from '~/pages/connexion.vue';

const emit = defineEmits(["handleValidate"]);

const handleSubmit = () => {
  emit("handleValidate");
}
</script>
  