<template>
  <h1 class="card-title pb-4 text-neutral mt-6">{{title}}</h1>
  <h2 class="pb-4 text-accent text-sm">{{subTitle}}</h2>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <div v-for="(student, index) in state.group" class="w-fit" :key="'student-' + index + '-'  + state.group.length" >
      <h3 class="ml-2 mb-2 font-bold">{{ "Personne " + (index + 1) }}</h3>
      <AutoComplete v-model:selected="state.group[index]" :peoples="state.availableStudents" :default-value="student" @update:selected="getAvailableStudents" @delete="deletePerson(index)"></AutoComplete>
    </div>

    <div class="mt-8">
      <ImageButton v-if="getStudentsInGroup().length !== state.allStudents.length " :src="ButtonPlus" class="shadow-md min-h-[2.5rem] h-[2.5rem]" @click="addPerson">Ajouter un membre</ImageButton>
    </div>
  </div>
</template>

<script setup>
import ButtonPlus from "@/assets/images/plus.png"
import axios from "axios";

const props = defineProps({
    title: String,
    subTitle: String
  });

const route = useRoute();


const state = reactive({
    sessionName: "Projet TIC 2024",
    allStudents: [],
    availableStudents: [],
    group: [],
    groups: [
        {
            students:[
                { id: 3, firstname: 'Devon', name: 'Webb', email: "devon.webb@example.com" },
                { id: 4, firstname:'Tom', name: 'Cook', email: "tom.cook@example.com" },
                { id: 6, firstname: 'Tanya', name: 'Fox', email: "tanya.fox@example.com" },
            ]
        },
        {
            students:[
                { id: 7, firstname: 'Didi', name: 'Cook', email: "devon.webb@example.com" },
                { id: 8, firstname:'Dada', name: 'Web', email: "tom.cook@example.com" },
                { id: 9, firstname: 'Tan', name: 'Test', email: "tanya.fox@example.com" },
            ]
        },
        {
            students:[
                { id: 10, firstname:'Wally', name:"Coop", email: "wade.cooper@example.com" },
                { id: 11, firstname: "Hélène", name:"Coy", email: "arlene.mccoy@example.com" },
                { id: 12, firstname:'Tom', name: 'Cook', email: "tom.cook@example.com" },
            ]
        }
    ]
  })
  

  onMounted(() => {
    getAvailableStudents();
  })

  const addPerson = () => {
    if(getStudentsInGroup().length === state.allStudents.length) return;
    state.group.push(state.availableStudents[0])
  }

  const deletePerson = (index) => {
    state.group.splice(index, 1)
    getAvailableStudents();
  }

  const getStudentsInGroup = () => state.groups.map(group => group.students).flat().concat(state.group)

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

  const getAllStudents = async () => {
    try {
      console.log(route.params.sessionId)
      const data = {
        sessionID: route.params.sessionId
      }

      const jsonData = JSON.stringify(data);

      const res = await axios.post(
        "http://127.0.0.1:5000/api/get_all_students",
        jsonData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      
      console.log(res.data)
      state.allStudents = res.data
    } catch (err) {
      console.log("error")
      console.error(err);
    }
  }

  const createGroup = async () => {
    try {
      console.log(state.group)
      const data = [
            {'studentID': 1},
            {'studentID': 2}
        ]     

        const jsonData = JSON.stringify(data);
      const res = await axios.post(
        "http://127.0.0.1:5000/api/create_group",
        state.group,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      state.allStudents = res.data
    } catch (err) {
      console.error(err);
    }
  }

  onMounted(async () => {
     await getAllStudents();
  })

  const validateGroup = async () => {
    console.log(state.group)

    //await navigateTo('/createGroupConfirmation')
  }
</script>
