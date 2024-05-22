<template>
  <div class="flex flex-col md:flex-row justify-center items-center h-[100vh]">
    <img class="w-[50%] md:w-[300px]" src="../public/learning.svg" alt="" />
    <div class="m-3 md:m-9">
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
            <div>
              <h2 class="m-3">Email</h2>
              <input type="text" class="input input-bordered w-full max-w-xs" />
            </div>
            <div>
              <h2 class="m-3">Mot de passe</h2>
              <input type="text" class="input input-bordered w-full max-w-xs" />
            </div>
          </div>
        </div>
        <div class="flex flex-col justify-center m-8">
          <h3 class="text-center m-1">Vous n'avez pas de compte?</h3>
          <a class="link text-center w-full" href="">Créer un compte</a>
        </div>
      </Card>
      <div class="flex justify-center mt-5">
        <ButtonPrimary>Connexion</ButtonPrimary>
      </div>
    </div>
    <img class="hidden md:block w-[350px]" src="../public/maths.svg" alt="" />
  </div>
</template>
<script setup></script>
