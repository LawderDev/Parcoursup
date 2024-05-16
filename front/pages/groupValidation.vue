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
                <ModalCreateGroup></ModalCreateGroup>
            </div>
             
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-7">
                <Card v-for="(group, index) in state.groups" :key="group.name" class="w-full flex items-center">
                    <div class="flex flex-col items-center gap-4">
                        <h3 class="card-title text-primary">{{ group.name }} ({{ group.students.length }})</h3>
                        <div class="flex flex-col gap-2">
                            <div class="flex gap-4" v-for="(student, index) in group.students" :key="'student-' + index + '-' + group.students.length">
                                <AutoComplete v-model:selected="group.students[index]" :peoples="state.availableStudents" :default-value="student" @update:selected="getAvailableStudents" @delete="deletePerson(index, group)"></AutoComplete>
                            </div>
                        </div>
                        <ButtonAdd v-if="getStudentsInGroup().length !== state.allStudents.length" @click="addPerson(group)">Ajouter un membre</ButtonAdd>
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
    allStudents: [
                { id: 1, firstname:'Wade', name:"Cooper", email: "wade.cooper@example.com" },
                { id: 2, firstname: 'Arlene', name:"Mccoy", email: "arlene.mccoy@example.com" },
                { id: 3, firstname: 'Devon', name: 'Webb', email: "devon.webb@example.com" },
                { id: 5, firstname: 'Love', name: 'Fox', email: "tanya.fox@example.com" },
                { id: 3, firstname: 'Devon', name: 'Webb', email: "devon.webb@example.com" },
                { id: 4, firstname:'Tom', name: 'Cook', email: "tom.cook@example.com" },
                { id: 6, firstname: 'Tanya', name: 'Fox', email: "tanya.fox@example.com" },
                { id: 7, firstname: 'Didi', name: 'Cook', email: "devon.webb@example.com" },
                { id: 8, firstname:'Dada', name: 'Web', email: "tom.cook@example.com" },
                { id: 9, firstname: 'Tan', name: 'Test', email: "tanya.fox@example.com" },
                { id: 10, firstname:'Wally', name:"Coop", email: "wade.cooper@example.com" },
                { id: 11, firstname: "Hélène", name:"Coy", email: "arlene.mccoy@example.com" },
                { id: 12, firstname:'Tom', name: 'Cook', email: "tom.cook@example.com" },
    ],
    availableStudents: [],
    groups: [
        {
            name: "Groupe 1",
            students:[
                { id: 1, firstname:'Wade', name:"Cooper", email: "wade.cooper@example.com" },
                { id: 2, firstname: 'Arlene', name:"Mccoy", email: "arlene.mccoy@example.com" },
                { id: 3, firstname: 'Devon', name: 'Webb', email: "devon.webb@example.com" },
                { id: 5, firstname: 'Love', name: 'Fox', email: "tanya.fox@example.com" },
            ]
        },
        {
            name: "Groupe 2",
            students:[
                { id: 3, firstname: 'Devon', name: 'Webb', email: "devon.webb@example.com" },
                { id: 4, firstname:'Tom', name: 'Cook', email: "tom.cook@example.com" },
                { id: 6, firstname: 'Tanya', name: 'Fox', email: "tanya.fox@example.com" },
            ]
        },
        {
            name: "Groupe 3",
            students:[
                { id: 7, firstname: 'Didi', name: 'Cook', email: "devon.webb@example.com" },
                { id: 8, firstname:'Dada', name: 'Web', email: "tom.cook@example.com" },
                { id: 9, firstname: 'Tan', name: 'Test', email: "tanya.fox@example.com" },
            ]
        },
        {
            name: "Groupe 4",
            students:[
                { id: 10, firstname:'Wally', name:"Coop", email: "wade.cooper@example.com" },
                { id: 11, firstname: "Hélène", name:"Coy", email: "arlene.mccoy@example.com" },
                { id: 12, firstname:'Tom', name: 'Cook', email: "tom.cook@example.com" },
            ]
        }
    ]
  })

  onMounted(() => {
    console.log(state.groups)
    getAvailableStudents();
  })

  const addPerson = (group) => {
    console.log(getStudentsInGroup().length)
    console.log(state.allStudents.length)
    if(getStudentsInGroup().length === state.allStudents.length) return;
    group.students.push(state.availableStudents[0])
  }

  const deletePerson = (index, group) => {
    group.students.splice(index, 1)
    getAvailableStudents();
  }

  const getStudentsInGroup = () => state.groups.map(group => group.students).flat()

  const getAvailableStudents = () => {
    const studentsInGroup = getStudentsInGroup();

    const availableStudents = state.allStudents.filter(stud => {
        return !studentsInGroup.some(s => s && s.id === stud.id);
    });

    state.availableStudents = availableStudents
  }

  const handleEditGroup = (group) => {
    console.log(group)
  }
  </script>
  