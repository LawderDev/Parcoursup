<template>
    <div>
      <div>
        <h2 class="text-3xl my-8 font-extrabold text-center">{{title}}</h2>
        <h3 class="ml-2 text-secondary text-center md:hidden">{{ subTitleMobile }}</h3>
        <h3 class="ml-2 text-secondary text-center hidden md:block">{{ subTitle }}</h3>
      </div>
      <div class="flex justify-center mt-8">
          <Card class="h-[65vh] w-[95vw] mt-6 md:w-[580px] overflow-y-scroll" no-fit>
              <div class="flex justify-center items-center">
                <img src="../public/confirmation.svg" alt="confirmation" class="w-36 h-36"/>
              </div>
              <h2 class="text-xl my-4 font-bold ml-2 text-center">{{cardTitle}}</h2>
              <div v-for="assignation in assignations" class="flex gap-2 items-center mb-4 hidden md:flex ">
                <div class="flex-auto justify-start btn min-h-2 h-10 rounded-full neumorphism">
                    <span class="text-xs font-bold flex-auto text-neutral">{{ assignation.group.nom }}</span>
                    
                    <Tooltip :content="assignation.group.description">...</Tooltip>
                </div>
                <img class="h-8 w-8" alt="arrow-right" src="@/public/arrow-right.svg"/>
                <div class="flex-auto justify-start btn min-h-2 h-10 rounded-full neumorphism">
                    <span class="text-xs font-bold flex-auto text-neutral">{{ assignation.project.nom}}</span>
                    <Tooltip :content="assignation.project.description">?</Tooltip>
                </div>
              </div>
              <ButtonPrimary @click="handleDownload">{{ downloadButton }}</ButtonPrimary>
              <ButtonSecondary @click="sendMailsResult">{{ sendMails }}</ButtonSecondary>
          </Card>
      </div>
      <div class="flex justify-center">
        <div class="flex justify-start md:w-[580px] mt-5">
          <ButtonSecondary @click="$emit('handleButtonClick')">{{buttonTitle}}</ButtonSecondary>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
import axios from 'axios';
import { useToasterStore } from '@/stores/toaster';

const config = useRuntimeConfig();
const toaster = useToasterStore();


 const props = defineProps({
    title: String,
    subTitleMobile: String,
    subTitle: String,
    cardTitle: String,
    downloadButton: String,
    sendMails: String,
    buttonTitle: String,
    nbSteps: Number,
    nbStepsActive: Number,
    nbStepsLock: Number,
    assignations: Array,
    formatGroupsAssignations: Array,
  })

  const handleDownload = () => {
     // Le texte à télécharger
     const textToDownload = props.assignations.map((assignation) => `${assignation.group.nom} (${assignation.group.description.replace(/\n/g, '')}) ------> ${assignation.project.nom}`).join('\n');

    // Crée un Blob avec le contenu texte
    const blob = new Blob([textToDownload], { type: 'text/plain' });

    // Crée un lien de téléchargement
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'assignations.txt';

    // Ajoute le lien au document et clique dessus pour démarrer le téléchargement
    document.body.appendChild(link);
    link.click();

    // Supprime le lien du document
    document.body.removeChild(link);
  }

 const sendMailsResult = async () => {
    console.log(props.formatGroupsAssignations)

    try{
      await axios.post(`${config.public.backUrl}/api/send_mail_result`, props.formatGroupsAssignations)
      toaster.showMessage("Les emails ont bien été envoyé !", "success");
    }
    catch(error){
      toaster.showMessage("Erreur lors de l'envoi des emails, vérifiez votre serveur SMTP", "error");
      console.error(error)
    }
  }

  defineEmits(['handleButtonClick'])
  </script>
