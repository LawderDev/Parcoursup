<template>
  <h1 class="card-title pb-4 text-neutral mt-6">{{title}}</h1>
  <h2 class="pb-4 text-accent text-sm">{{subTitle}}</h2>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <div v-for="(_, index) in group" class="w-fit" :key="'student-' + index + '-'  + group.length">
      <h3 class="ml-2 mb-2 font-bold">{{ "Personne " + (index + 1) }}</h3>
      <AutoComplete v-if="state.loading" :selected="group[index]" :peoples="state.availableStudents" :default-value="group[index] ? group[index] : state.availableStudents[0]" @update:selected="handleSelected($event, index)" @delete="deletePerson(index)"></AutoComplete>
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
    subTitle: String,
    group: Array,
  });

const emit = defineEmits(['update:group']);

const route = useRoute();

onMounted(async () => {
    await getAllGroups();
    await getAllStudents();
    await getAvailableStudents();
    state.loading = true;
})

const state = reactive({
    sessionName: "Projet TIC 2024",
    allStudents: [],
    availableStudents: [],
    groups: [],
    loading:false,
  })

  const addPerson = () => {
    if(getStudentsInGroup().length === state.allStudents.length) return;
    emit("update:group", props.group.concat(state.availableStudents[0]))
    getAvailableStudents();
  }

  const deletePerson = (index) => {
    emit("update:group", props.group.filter((_, i) => i !== index))
    getAvailableStudents();
  }

  const getStudentsInGroup = () => state.groups.map(group => group.students).flat().concat(props.group).filter(s => s)

  const getAvailableStudents = () => {
    const studentsInGroup = getStudentsInGroup();
    const availableStudents = state.allStudents.filter(stud => {
        return !studentsInGroup.some(s => s && s.id === stud.id);
    });

    state.availableStudents = availableStudents
  }

  const handleSelected = (student, index) => {
    emit("update:group", props.group.map((s, i) => i === index ? student : s))
    nextTick(() => getAvailableStudents());
  }

  const getAllGroups = async () => {
    try {
      const data = {
        sessionID: route.params.sessionId
      }

      const jsonData = JSON.stringify(data);

      const res = await axios.post(
        "http://127.0.0.1:5000/api/get_all_groups_students",
        jsonData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      
      console.log(res.data)
      state.groups = res.data
    } catch (err) {
      console.log("error")
      console.error(err);
    }
  }

  const getAllStudents = async () => {
    try {
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
      
      state.allStudents = res.data
    } catch (err) {
      console.log("error")
      console.error(err);
    }
  }
</script>
