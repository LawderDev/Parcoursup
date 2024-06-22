<template>
   <Modal @close="$emit('update:isOpen', false)">
        <template v-slot:open-btn>
           <div class="hidden" ref="openBtn"></div>
        </template>
        <template v-slot:form>
            <h2 class="font-semibold text-primary text-center mb-5 text-xl">Supprimer une session</h2>
            <Ranking :items="state.groups" description="Classez les groupes de projets en fonction de vos préférences"></Ranking>
        </template>
        <template v-slot:action>
            <button class="mt-5">
              <ButtonPrimary @click="handleSubmit" title="Valider">Valider</ButtonPrimary>
          </button>
        </template>
   </Modal>
  </template>
<script setup>
import axios from "axios";

const openBtn = ref(null);

const props = defineProps({
  isOpen: Boolean,
  projectId: Number,
  sessionId: Number,
})

const config = useRuntimeConfig()

const emit = defineEmits(["update:isOpen"]);

const state = reactive({
        groups : [],
  })

  const getGroups = async () => {
    try {
      const data = {
            "sessionID" : props.sessionId,
            "projectID" : props.projectId,
        };
      const jsonData = JSON.stringify(data);

      const response = await axios.post(`${config.public.backUrl}/api/get_project_groups_order_by_preferencies`, jsonData, {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );

      let sortedData = [...response.data];

      sortedData.sort((a, b) => a.id - b.id);

      sortedData.forEach((item, index) => {
          item.nom = `Groupe ${index + 1}`;
      });

      state.groups =  response.data.map(group => {
          return {
            id : group.id,
            nom : sortedData.find(element => element.id === group.id).nom,
            description: group.students.map(student => `${student.name} ${student.firstname}`).join(",\n ")
          }
      });

      // Afficher le tableau modifié
    } catch (error) {
      console.error(error);
    }
  }

  watch(
    () => props.projectId,
    async () => {
      await getGroups();
  })

  watch(
    () => props.isOpen,
    () => {
      if (props.isOpen) {
        openBtn.value.click();
      }
    })

  const handleSubmit = async () => {
    const data = {
        "data": state.groups.map((group, index) => {
          return {
            "projectID": props.projectId,
            "groupID": group.id,
            "order": index + 1
          }
        })
    }
    
    const jsonData = JSON.stringify(data);

    await axios.post(
      `${config.public.backUrl}/api/affect_preference_projet`,
      jsonData,
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    )

    emit("update:isOpen", false);
  }
  </script>
  