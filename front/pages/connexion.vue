<template>
  <div class="flex flex-col lg:flex-row justify-center items-center h-[100vh]">
    <img
      class="w-[25%] lg:block lg:w-[300px]"
      src="../public/learning.svg"
      alt=""
    />
    <div class="lg:m-9">
      <Card class="">
        <div class="m-0">
          <h2 class="text-3xl my-4 font-bold text-center text-primary">
            Connexion
          </h2>
          <h3 class="my-4 text-secondary text-center">
            Connectez-vous pour accéder à votre espace
          </h3>
        </div>
        <div class="flex justify-center">
          <div>
            <div v-if="!state.loginError">
              <h2 class="m-3">Email</h2>
              <input
                v-model="state.login"
                type="email"
                class="input input-bordered w-full max-w-xs"
              />
            </div>
            <div v-else>
              <h2 class="m-3 text-error">Email</h2>
              <input
                v-model="state.login"
                type="email"
                class="input input-bordered input-error w-full max-w-xs"
              />
              <span class="label label-text-alt text-error"
                >Adresse mail incorrect</span
              >
            </div>
            <div>
              <div v-if="!state.passwordError">
                <h2 class="m-3">Mot de passe</h2>
                <input
                  v-model="state.password"
                  type="password"
                  class="input input-bordered w-full max-w-xs"
                />
              </div>
              <div v-else>
                <h2 class="m-3 text-error">Mot de passe</h2>
                <input
                  v-model="state.password"
                  type="password"
                  class="input input-bordered input-error w-full max-w-xs"
                />
                <span class="label label-text-alt text-error"
                  >Mot de passe incorrect</span
                >
              </div>
            </div>
          </div>
        </div>
        <div class="flex flex-col justify-center m-8">
          <h3 class="text-center m-1">Vous n'avez pas de compte?</h3>
          <a class="link text-center w-full" href="">Créer un compte</a>
        </div>
      </Card>
      <div class="flex justify-center mt-5">
        <ButtonPrimary @click="openIndexPage">Connexion</ButtonPrimary>
      </div>
    </div>
    <div class="hidden lg:m-9">
      <Card>
        <div class="m-4">
          <h2 class="text-3xl m-4 font-bold text-center text-primary">
            Connexion
          </h2>
          <h3 class="m-4 text-secondary text-center">
            Connectez-vous pour accéder à votre espace
          </h3>
        </div>
        <div class="flex justify-center">
          <div>
            <div v-if="!state.loginError">
              <h2 class="m-3">Email</h2>
              <input
                v-model="state.login"
                type="email"
                class="input input-bordered w-full max-w-xs"
              />
            </div>
            <div v-else>
              <h2 class="m-3 text-error">Email</h2>
              <input
                v-model="state.login"
                type="email"
                class="input input-bordered input-error w-full max-w-xs"
              />
              <span class="label label-text-alt text-error"
                >Adresse mail incorrect</span
              >
            </div>
            <div>
              <div v-if="!state.passwordError">
                <h2 class="m-3">Mot de passe</h2>
                <input
                  v-model="state.password"
                  type="password"
                  class="input input-bordered w-full max-w-xs"
                />
              </div>
              <div v-else>
                <h2 class="m-3 text-error">Mot de passe</h2>
                <input
                  v-model="state.password"
                  type="password"
                  class="input input-bordered input-error w-full max-w-xs"
                />
                <span class="label label-text-alt text-error"
                  >Mot de passe incorrect</span
                >
              </div>
            </div>
          </div>
        </div>
        <div class="flex flex-col justify-center m-8">
          <h3 class="text-center m-1">Vous n'avez pas de compte?</h3>
          <a class="link text-center w-full" href="">Créer un compte</a>
        </div>
      </Card>
      <div class="flex justify-center mt-5">
        <ButtonPrimary @click="openIndexPage">Connexion</ButtonPrimary>
      </div>
    </div>
    <img class="hidden lg:block w-[350px]" src="../public/maths.svg" alt="" />
  </div>
</template>
<script setup>
import { useToasterStore } from "~/stores/toaster";
import axios from "axios";
const toaster = useToasterStore();
const state = reactive({
  login: null,
  password: null,
  loginError: false,
  passwordError: false,
});
const openIndexPage = async () => {
  state.loginError =false
  state.passwordError =false
  const res = await callLogin()
  if (res.status===200) {
    toaster.showMessage("Connexion réussie", "success");
    await navigateTo("/");
  } else if (res.status===401){
    handleError(res.data.message)
  }else{
    showErrorUnknown()
  }
};
const handleError = (message) => {
  if(message.includes('login')){
    state.loginError = true
  }else if (message.includes('password')){
    state.passwordError = true
  } else{
    showErrorUnknown()
  }
}
const showErrorUnknown = () => {
  toaster.showMessage("Erreur inconnue de lors de l'authentification", "error");
}
const callLogin = async () => {
  try {
    const jsonData = getJsonData(state.login, state.password);
    const res = await axios.post("http://127.0.0.1:5000/api/login", jsonData, {
      headers: {
        "Content-Type": "application/json",
      },
    });
    return res;
  } catch (err) {
    return err.response
  }
};
const getJsonData = (login, password) => {
  const data = {
    data: [
      {
        Email: state.login,
        Password: state.password,
      },
    ],
  };
  return JSON.stringify(data);
};
watch(
  () => state.password,
  () => {
    if (state.password.length) {
    }
  }
);
</script>
