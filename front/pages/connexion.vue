<template>
  <div class=" flex justify-center items-center h-[100vh]">
    <div class=" ">
      <Card>
        <div>
          <h2 class="text-3xl my-8 font-bold text-center text-primary">
            Connexion
          </h2>
          <h3 class="m-5 text-secondary text-center">
            Connectez-vous pour accéder à votre espace
          </h3>
        </div>
        <div class="flex justify-center">
          <div>
            <div>
              <h2 class="ml-1 my-5">Email</h2>
              <input type="text" class="input input-bordered w-full max-w-xs" />
            </div>
            <div>
              <h2 class="ml-1 my-5">Mot de passe</h2>
              <input type="text" class="input input-bordered w-full max-w-xs" />
            </div>
          </div>
        </div>
        <div class="flex justify-center">
          <div class="flex justify-center md:w-[580px] mt-5">
            <ButtonPrimary>Connexion</ButtonPrimary>
          </div>
        </div>
        <div class="flex justify-center">
          <div>
            <h3>Vous n'avez pas de compte?</h3>
            <a class="link" href="">Créer un compte</a>
          </div>
        </div>
      </Card>
    </div>
  </div>
</template>
