<template>
    <div>
      <Modal>
        <template v-slot:open-btn>
          <ButtonPrimary @click="resetForm">Ajouter un utilisateur</ButtonPrimary>
        </template>
        <template v-slot:form>
            <div class="w-[75vw] md:w-[35vw]">
                <h1 class="font-semibold text-primary text-center p-4 text-xl">
                    Ajouter un utilisateur
                </h1>
                <div>
                    <h2 class="mb-2">Nom</h2>
                    <div class="flex flex-col w-full mb-5">
                        <input v-model="state.name.value" class="input input-bordered w-full rounded-badge" :class="{'input-error': !state.name.isValid}"/>
                        <span v-if="!state.name.isValid" class="label label-text-alt text-error">{{ state.name.errorMessage }}</span>
                    </div>
                </div>
                <div>
                    <h2 class="mb-2">Prénom</h2>
                    <div class="flex flex-col w-full mb-5">
                        <input v-model="state.firstname.value" class="input input-bordered w-full rounded-badge" :class="{'input-error': !state.firstname.isValid}"/>
                        <span v-if="!state.firstname.isValid" class="label label-text-alt text-error">{{ state.firstname.errorMessage }}</span>
                    </div>
                </div>
                <div>
                    <h2 class="mb-2">Email</h2>
                    <div class="flex flex-col w-full mb-5">
                        <input v-model="state.email.value" class="input input-bordered w-full rounded-badge" :class="{'input-error': !state.email.isValid}"/>
                        <span v-if="!state.email.isValid" class="label label-text-alt text-error">{{ state.email.errorMessage }}</span>
                    </div>
                </div>
                <div>
                    <h2 class="mb-2">Mot de passe</h2>
                    <div class="flex flex-col w-full mb-5">
                        <input v-model="state.password.value" type="password" class="input input-bordered w-full rounded-badge" :class="{'input-error': !state.password.isValid}"/>
                        <span v-if="!state.password.isValid" class="label label-text-alt text-error">{{ state.password.errorMessage }}</span>
                    </div>
                </div>
                <div>
                    <h2 class="mb-2">Confirmer le mot de passe</h2>
                    <div class="flex flex-col w-full mb-5">
                        <input v-model="state.confirmPassword.value" type="password" class="input input-bordered w-full rounded-badge" :class="{'input-error': !state.confirmPassword.isValid}"/>
                        <span v-if="!state.confirmPassword.isValid" class="label label-text-alt text-error">{{ state.confirmPassword.errorMessage }}</span>
                    </div>
                </div>
            </div>
        </template>
        <template v-slot:action>
            <ButtonPrimary @click="handleSubmit" title="Valider">Valider</ButtonPrimary>
            <button class="hidden" ref="closeBtn"></button>
        </template>
      </Modal>
    </div>
</template>
<script setup>
import axios from "axios";
import { useToasterStore } from '@/stores/toaster';

const toaster = useToasterStore();
const config = useRuntimeConfig();

const emit = defineEmits(["handleValidate"]);

const state = reactive({
    name: {
        value: "",
        isValid: true,
        errorMessage: "Veuillez renseigner le nom",
    },
    firstname: {
        value: "",
        isValid: true,
        errorMessage: "Veuillez renseigner le prénom",
    },
    email: {
        value: "",
        isValid: true,
        errorMessage: "Veuillez renseigner l'email",
    },
    password: {
        value: "",
        isValid: true,
        errorMessage: "Veuillez renseigner le mot de passe",
    },
    confirmPassword: {
        value: "",
        isValid: true,
        errorMessage: "Veuillez renseigner le mot de passe",
    },
})

const closeBtn = ref(null);

const createUser = async () => {
    const data = { 
        "data" : [
            {
                'Nom': state.name.value,
                'Prenom': state.firstname.value,
                'Email': state.email.value, 
                'Password': state.password.value,
            }
        ]     
        };

    const jsonData = JSON.stringify(data);
            
    // User registration
    await axios.post(`${config.public.backUrl}/api/register`,jsonData, {
        headers: {
            'Content-Type': 'application/json'
         }
    })
}

const resetForm = () => {
    state.name.value = "";
    state.name.isValid = true;
    state.firstname.value = "";
    state.firstname.isValid = true;
    state.email.value = "";
    state.email.isValid = true;
    state.password.value = "";
    state.password.isValid = true;
    state.confirmPassword.value = "";
    state.confirmPassword.isValid = true;
}

const handleSubmit =  async () => {
    state.name.isValid = state.name.value !== "";
    state.firstname.isValid = state.firstname.value !== "";
    state.email.isValid = state.email.value !== "";
    state.password.isValid = state.password.value !== "";
    state.confirmPassword.isValid = state.confirmPassword.value !== "";

    let isError = false;
    
    if(!state.name.isValid || !state.firstname.isValid || !state.email.isValid || !state.password.isValid || !state.confirmPassword.isValid) {
        state.password.errorMessage = "Veuillez renseigner le mot de passe";
        state.confirmPassword.errorMessage = "Veuillez renseigner le mot de passe";
        isError = true;
    }

    if(state.password.value !== state.confirmPassword.value) {
        state.password.isValid = false;
        state.confirmPassword.isValid = false;
        state.password.errorMessage = "Les mots de passe ne sont pas identiques";
        state.confirmPassword.errorMessage = "Les mots de passe ne sont pas identiques";
        isError = true;
    }

    if(isError) {
        toaster.showMessage("Erreur lors de l'ajout de l'utilisateur", "error");
        return;
    }

    closeBtn.value.click();
    await createUser();
    emit("handleValidate");
    toaster.showMessage("L'utilisateur a bien été ajouté", "success");
}
</script>
  