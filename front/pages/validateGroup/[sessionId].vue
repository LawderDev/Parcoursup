<template>
  <div>
    <NavBar name="M"></NavBar>
    <div class="mx-8 mt-10">
      <div class="flex flex-wrap">
        <h1
          class="text-3xl font-bold max-w-48 md:max-w-96 truncate tooltip tooltip-open mb-8"
          data-tip="Projet TIC 2024"
        >
          {{ state.sessionName }}
        </h1>
        <div class="flex ml-auto gap-4">
          <ButtonSecondary @click="handleBack">Retourner à la session</ButtonSecondary>

          <ButtonPrimary @click="handleValidateGroup">Valider les groupes</ButtonPrimary>
        </div>
      </div>
      <div class="flex gap-4 items-center mb-6">
        <h2 class="text-xl font-semibold">Groupes</h2>
        <ModalCreateGroup @handle-create-group="refreshGroups"></ModalCreateGroup>
        <ButtonPrimary @click="handleSave">Enregistrer</ButtonPrimary>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-7">
        <Card
          v-for="(group, index) in state.groups"
          :key="group.name"
          class="w-full flex items-center"
        >
          <div class="flex flex-col items-center gap-4">
            <h3 class="card-title text-primary">
              {{ group.name }} ({{ group.students.length }})
            </h3>
            <div class="flex flex-col gap-2">
              <div
                class="flex gap-4"
                v-for="(student, index) in group.students"
                :key="'student-' + index + '-' + group.students.length"
              >
                <AutoComplete
                  v-model:selected="group.students[index]"
                  :peoples="state.availableStudents"
                  :default-value="student"
                  @update:selected="getAvailableStudents"
                  @delete="deletePerson(index, group)"
                ></AutoComplete>
              </div>
            </div>
            <ButtonAdd
              v-if="getStudentsInGroup().length !== state.allStudents.length"
              @click="addPerson(group)"
              >Ajouter un membre</ButtonAdd
            >
            <ButtonSecondary>Supprimer</ButtonSecondary>
          </div>
        </Card>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";

const state = reactive({
  sessionName: "Projet TIC 2024",
  allStudents: [],
  availableStudents: [],
  groups: [],
});

const route = useRoute();

onMounted(async () => {
 state.groups = await getAllGroups();
  await getAllStudents();
  await getAvailableStudents();
  state.loading = true;
});

const refreshGroups = async () => {
    state.groups = await getAllGroups();
    await getAvailableStudents();
};

const addPerson = (group) => {
  console.log(getStudentsInGroup().length);
  console.log(state.allStudents.length);
  if (getStudentsInGroup().length === state.allStudents.length) return;
  group.students.push(state.availableStudents[0]);
};

const deletePerson = (index, group) => {
  group.students.splice(index, 1);
  getAvailableStudents();
};

const getStudentsInGroup = () =>
  state.groups.map((group) => group.students).flat();

/*const getStudentsInGroup = () => state.groups.map(group => group.students).flat().concat(props.group).filter(s => s)

  const getAvailableStudents = () => {
    const studentsInGroup = getStudentsInGroup();
    const availableStudents = state.allStudents.filter(stud => {
        return !studentsInGroup.some(s => s && s.id === stud.id);
    });

    state.availableStudents = availableStudents
  }*/

const getAvailableStudents = () => {
  const studentsInGroup = getStudentsInGroup();

  const availableStudents = state.allStudents.filter((stud) => {
    return !studentsInGroup.some((s) => s && s.id === stud.id);
  });

  state.availableStudents = availableStudents;
};

const handleEditGroup = (group) => {
  console.log(group);
};

const getAllGroups = async () => {
  try {
    const data = {
      sessionID: route.params.sessionId,
    };

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

    return res.data;
  } catch (err) {
    console.log("error");
    console.error(err);
  }
};

const getAllStudents = async () => {
  try {
    const data = {
      sessionID: route.params.sessionId,
    };

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

    state.allStudents = res.data;
  } catch (err) {
    console.log("error");
    console.error(err);
  }
};

const handleBack = async() => {
  await navigateTo(`/session/${route.params.sessionId}`);
}

const reafectGroup = async (data) => {

    const jsonData = JSON.stringify({ data: data})

    console.log(jsonData)
    await axios.post("http://127.0.0.1:5000/api/reaffect_group", jsonData, {
        headers: {
           'Content-Type': 'application/json'
        }}
    );
}

const handleSave = async () => {
    const oldGroup = await getAllGroups();
        
    const studentsToReassign = []

    state.groups.forEach((group) => {
        oldGroup.forEach((oldGroup) => {
            if (group.id === oldGroup.id) {
                let students = group.students.filter((student) => !oldGroup.students.some((oldStudent) => oldStudent.id === student.id));
                students.forEach((student) => {
                    studentsToReassign.push({
                        id_student: student.id,
                        id_new_group: group.id
                    })
                })
            }
        })
    })

    if(studentsToReassign.length === 0) return

    await reafectGroup(studentsToReassign);
}

const validateGroups = async () => {
   //TODO CHANGE STATE SESSION TO CHOOSING
}

const handleValidateGroup = async () => {
    await handleSave();
    await validateGroups();

}
</script>
