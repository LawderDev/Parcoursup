<template>
  <div>
    <Modal @close="$emit('update:isOpen', false)">
      <template v-slot:open-btn>
        <li class="pl-1 button">
          <div class="flex items-center">
            <img src="../public/settings.svg" class="w-5" />
            <a class="md:text-lg">Profil</a>
          </div>
        </li>
      </template>
      <template v-slot:form>
        <div class="m-5">
          <div class="flex justify-center">
            <h1 class="text-2xl text-primary">Profil</h1>
          </div>
          <div>
            <div>
              <h2 class="m-3">Nom</h2>
              <input
                v-model="state.name"
                type="text"
                class="input input-bordered w-full max-w-xs"
              />
            </div>
            <div>
              <h2 class="m-3">Prénom</h2>
              <input
                v-model="state.firstname"
                type="text"
                class="input input-bordered w-full max-w-xs"
              />
            </div>
            <div>
              <h2 class="m-3">Email</h2>
              <input
                v-model="state.email"
                type="email"
                class="input input-bordered w-full max-w-xs"
              />
            </div>
            <div v-if="state.editPassword">
              <div>
                <h2
                  class="m-3"
                  :class="{
                    'text-error': state.errorPassword && state.editPassword,
                  }"
                >
                  Ancien mot de passe
                </h2>
                <input
                  v-model="state.password"
                  type="password"
                  :class="[
                    'input input-bordered w-full max-w-xs',
                    {
                      'input-error': state.errorPassword,
                    },
                  ]"
                />
              </div>
              <div>
                <h2 class="m-3" :class="{ 'text-error': state.errorPassword }">
                  Nouveau mot de passe
                </h2>
                <input
                  v-model="state.newPassword"
                  type="password"
                  :class="[
                    'input input-bordered w-full max-w-xs',
                    { 'input-error': state.errorPassword },
                  ]"
                />
              </div>
              <div class="label">
                <span class="label-text-alt">
                  Le mot de passe doit être différent du précédent et contenir
                  au moins 8 caractères
                </span>
              </div>
              <div class="flex justify-center">
                <div>
                  <EditInput
                    v-show="state.newPassword.length && state.password.length"
                    :src="OkClickable"
                    @click="handleSubmitNewPassword"
                  ></EditInput>
                  <EditInput
                    :src="Cancel"
                    @click="handleEditCancel"
                  ></EditInput>
                </div>
              </div>
            </div>
          </div>
          <div class="mt-4" v-if="!state.editPassword">
            <h3 class="text-center m-1">
              Voulez-vous changer de
              <a class="link" @click="handleEditPassword">mot de passe?</a>
            </h3>
          </div>
        </div>
      </template>
      <template v-slot:action>
        <!-- Ajouter les boutons d'action ici si nécessaire -->
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { reactive } from "vue";
import OkClickable from "~/public/okClickable.svg";
import Cancel from "~/public/cancel.svg";
import axios from "axios";
import bcrypt from "bcryptjs";

const state = reactive({
  name: "",
  firstname: "",
  email: "",
  password: "",
  newPassword: "",
  editPassword: false,
  errorPassword: false,
  hashedPassword: "",
});
const emit = defineEmits(["update:isOpen"]);
const handleSubmitNewPassword = async () => {
  if (passwordCorrect.value) {
    const res = await sendNewPassword();
    if (res && res.status===200) {
      state.password = "";
      state.newPassword = "";
      state.editPassword = false;
      state.errorFalse = false;
    }else{
      state.errorPassword = true
    }
  } else {
    state.errorPassword = true;
  }
};

const handleEditPassword = () => {
  state.editPassword = true;
};
const handleEditCancel = () => {
  state.editPassword = false;
  state.password = "";
  state.newPassword = "";
};
const passwordCorrect = computed(() => {
  return state.password !== state.newPassword && state.newPassword.length >= 8;
});
const sendNewPassword = async () => {
  try {
    const data = {
      data: [
        {
          current_password: state.password,
          new_password: state.newPassword,
        },
      ],
    };
    console.log("hashPassword(state.password)",hashPassword(state.password))
    const jsonData = JSON.stringify(data);
    const res = await axios.post(
      "http://127.0.0.1:5000/api/update_password",
      jsonData, {
      headers: {
        "Content-Type": "application/json",
      },
      withCredentials: true, // Ensure cookies are sent and received
    });
    return res;
  } catch (err) {
    console.error("Erreur lors du changement de mot de pass :", err);
  }
};
const getCurrentUserData = async () => {
  try {
    await callLogin();
    const response = await axios.get("http://127.0.0.1:5000/api/current_user", {
      withCredentials: true, // Ensure cookies are sent and received
    });
    console.log("response.data", response.data);
    return response.data;
  } catch (error) {
    console.error(
      "Erreur lors de la récupération des infos utilisateurs :",
      error
    );
  }
};
const callLogin = async () => {
  try {
    const jsonData = getJsonData("test@test16.com", "monMDP");
    const res = await axios.post("http://127.0.0.1:5000/api/login", jsonData, {
      headers: {
        "Content-Type": "application/json",
      },
      withCredentials: true, // Ensure cookies are sent and received
    });
    return res;
  } catch (err) {
    console.error("Erreur lors de la récupération du login :", err);
  }
};
const getJsonData = (login, password) => {
  const data = {
    data: [
      {
        Email: login,
        Password: password,
      },
    ],
  };
  return JSON.stringify(data);
};
const hashPassword = (password) => {
  const salt = bcrypt.genSaltSync(10);
  return bcrypt.hashSync(password, salt);
};
watch(
  () => state.editPassword,
  () => {
    state.errorPassword = false;
  }
);
onMounted(async () => {
  const data = await getCurrentUserData();
  state.firstname = data.Prenom;
  state.name = data.Nom;
  state.email = data.Email;
});
</script>
