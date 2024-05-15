<template>
    <div>
        <NavBar name="M"></NavBar>
        <div class="mx-8 mt-10">
            <div class="flex flex-wrap">
                <h1 class="text-3xl font-bold max-w-48 md:max-w-96 truncate tooltip tooltip-open mb-8" data-tip="Projet TIC 2024">
                    {{ state.sessionName }}
                </h1>
                <div class="flex ml-auto gap-4">
                    <ButtonSecondary>Retourner à la session</ButtonSecondary>
                
                    <ButtonPrimary>Valider les groupes</ButtonPrimary>
                </div>
            </div>
            <div class="flex gap-4 items-center mb-6">
                <h2 class="text-xl font-semibold">Groupes</h2>
                <ButtonAdd>Ajouter un groupe</ButtonAdd>
            </div>
             
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-7">
                <Card v-for="group in state.groups" :key="group.name" class="w-full flex items-center">
                    <div class="flex flex-col items-center gap-4">
                        <h3 class="card-title text-primary">{{ group.name }} ({{ group.students.length }})</h3>
                        <div class="flex flex-col gap-2">
                            <div  class="flex gap-4" v-for="(_,index) in group.students">
                                <AutoComplete v-model:selected="group.students[index]" :peoples="group.students" :default-index="index"></AutoComplete>
                                <button>
                                    <img src="@/public/minus.svg" alt="Image" class="w-6 h-6 mr-2">
                                </button>
                            </div>
                        </div>
                        <ButtonAdd>Ajouter un membre</ButtonAdd>
                        <div class="flex gap-4">
                            <ButtonSecondary>Supprimer</ButtonSecondary>
                            <ButtonPrimary @click="handleEditGroup(group)">Modifier</ButtonPrimary>
                        </div>
                    </div>
                </Card>
            </div>
            
            
        </div>
    </div>
</template>
  
  <script setup>


  const state = reactive({
    sessionName: "Projet TIC 2024",
    groups: [
        {
            name: "Groupe 1",
            students:[
                { id: 1, firstname:'Wade', name:"Cooper", email: "wade.cooper@example.com" },
                { id: 2, firstname: 'Arlene', name:"Mccoy", email: "arlene.mccoy@example.com" },
                { id: 3, firstname: 'Devon', name: 'Webb', email: "devon.webb@example.com" },
                { id: 4, firstname:'Tom', name: 'Cook', email: "tom.cook@example.com" },
                { id: 5, firstname: 'Tanya', name: 'Fox', email: "tanya.fox@example.com" },
            ]
        },
        {
            name: "Groupe 2",
            students:[
                { id: 1, firstname:'Wade', name:"Cooper", email: "wade.cooper@example.com" },
                { id: 2, firstname: 'FEZF', name:"MVAccoy", email: "arlene.mccoy@example.com" },
                { id: 3, firstname: 'Devon', name: 'Webb', email: "devon.webb@example.com" },
                { id: 4, firstname:'Tom', name: 'Cook', email: "tom.cook@example.com" },
                { id: 5, firstname: 'Tanya', name: 'Fox', email: "tanya.fox@example.com" },
            ]
        },
        {
            name: "Groupe 3",
            students:[
                { id: 1, firstname:'Wade', name:"CIJAPCAJF", email: "wade.cooper@example.com" },
                { id: 2, firstname: 'Arlene', name:"Mccoy", email: "arlene.mccoy@example.com" },
                { id: 3, firstname: 'Devon', name: 'Webb', email: "devon.webb@example.com" },
                { id: 4, firstname:'Tom', name: 'Cook', email: "tom.cook@example.com" },
                { id: 5, firstname: 'Tanya', name: 'Fox', email: "tanya.fox@example.com" },
            ]
        },
        {
            name: "Groupe 4",
            students:[
                { id: 1, firstname:'WADEIIEOO', name:"Cooper", email: "wade.cooper@example.com" },
                { id: 2, firstname: 'Arlene', name:"Mccoy", email: "arlene.mccoy@example.com" },
                { id: 3, firstname: 'Devon', name: 'Webb', email: "devon.webb@example.com" },
                { id: 4, firstname:'Tom', name: 'Cook', email: "tom.cook@example.com" },
                { id: 5, firstname: 'Tanya', name: 'Fox', email: "tanya.fox@example.com" },
            ]
        }
    ]
  })

  const handleEditGroup = (group) => {
    console.log(group)
  }
  </script>
  