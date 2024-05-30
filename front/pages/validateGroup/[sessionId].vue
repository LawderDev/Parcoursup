<template>
  <div>
    <NavBar></NavBar>
    <template v-if="state.isLoading">
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
          <ModalCreateGroup :key="'refreshModalCreateGroup' + state.groups.length" v-if="state.isLoading" @handle-create-group="refreshGroups" :groups="state.groups"></ModalCreateGroup>
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
                    :can-delete="true"
                    @update:selected="getAvailableStudents"
                    @delete="deletePerson(index, group)"
                  ></AutoComplete>
                </div>
              </div>
              {{  getStudentsInGroup().length }}
              {{ state.allStudents.length }}
              <ButtonAdd
                v-if="getStudentsInGroup().length !== state.allStudents.length"
                @click="addPerson(group)"
                >Ajouter un membre</ButtonAdd
              >
              <ButtonSecondary @click="handleDeleteGroup(group)">Supprimer</ButtonSecondary>
            </div>
          </Card>
        </div>
      </div>
    </template>
    <Skeleton v-else></Skeleton>
  </div>
</template>

<script setup>
import axios from "axios";
import { useSessionData } from "~/composables/useSessionData";
import { useToasterStore } from '@/stores/toaster';
import { useProject } from "~/composables/useProject";
import { useCreateGroup } from "~/composables/useCreateGroup";

const state = reactive({
  sessionName: "Projet TIC 2024",
  allStudents: [],
  availableStudents: [],
  groups: [],
  isLoading: false,
});

const config = useRuntimeConfig();

const toaster = useToasterStore();

const { stateProject, api_call_projects } = useProject();

const { stateSession, getSessionData, updateSession } = useSessionData(); 

const {stateCreateGroup, validateGroup} = useCreateGroup();

const route = useRoute();

onMounted(async () => {
  await getSessionData(route.params.sessionId);
  state.groups = await getAllGroups();
  await getAllStudents();
  await getAvailableStudents();
  await api_call_projects(route.params.sessionId);
  state.isLoading = true;
});

const refreshGroups = async (newGroup) => {
    state.groups.push(newGroup);
    await getAvailableStudents();
};

const addPerson = (group) => {
  if (getStudentsInGroup().length === state.allStudents.length) return;
  group.students.push(state.availableStudents[0]);
};

const deletePerson = (index, group) => {
  group.students.splice(index, 1);
  getAvailableStudents();
};

const getStudentsInGroup = () =>
  state.groups.map((group) => group.students).flat();

const getAvailableStudents = () => {
  const studentsInGroup = getStudentsInGroup();

  const availableStudents = state.allStudents.filter((stud) => {
    return !studentsInGroup.some((s) => s && s.id === stud.id);
  });

  state.availableStudents = availableStudents;
};

const getAllGroups = async () => {
  try {
    const data = {
      sessionID: route.params.sessionId,
    };

    const jsonData = JSON.stringify(data);

    const res = await axios.post(
      `${config.public.backUrl}/api/get_all_groups_students`,
      jsonData,
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    return res.data;
  } catch (err) {
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
      `${config.public.backUrl}/api/get_all_students`,
      jsonData,
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    state.allStudents = res.data;
  } catch (err) {
    console.error(err);
  }
};

const handleBack = async() => {
  await navigateTo(`/session/${route.params.sessionId}`);
}

const reafectGroup = async (data) => {

    const jsonData = JSON.stringify({ data: data})

    await axios.post(`${config.public.backUrl}/api/reaffect_group`, jsonData, {
        headers: {
           'Content-Type': 'application/json'
        }}
    );
}

const checkIfOneStudentInEachGroup = () => {
    const isOneStudent = state.groups.every((group) => group.students.length >= 1);
    if (!isOneStudent){
      toaster.showMessage("Veuillez renseigner au moins un etudiants dans chaque groupes", "error");
      return;
    } 
    return isOneStudent;
}

const deleteGroups = async (groups) => {
    try {
        await axios.post(`${config.public.backUrl}/api/delete_groups`, {
            groups: groups
        });
    } catch (error) {
        console.error("Erreur lors de la suppression du groupe", error);
    }
}

const handleSave = async () => {
    // Vérifie qu'il y a au moins un étudiants dans chaque groupe
    if(!checkIfOneStudentInEachGroup()) return;

    const oldGroups = await getAllGroups();

    // Supprime les groupes qui n'existent plus
    const groupsToDelete = oldGroups.filter((group) => !state.groups.some((oldGroup) => oldGroup.id === group.id));
    if(groupsToDelete.length > 0) await deleteGroups(groupsToDelete.map((group) => group.id));

    const studentsToReassign = []

    // Récupère les étudiants dont le groupe a changer
    state.groups.forEach((group) => {
        oldGroups.forEach((oldGroup) => {
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

    // Récupère les étudiants qui n'ont pas dans un groupe de base
    let newGroups = state.groups.map( async(group) => {
      if(group.id === null){
        return {
          id: (await validateGroup(group.students)).data.result[0],
          students: group.students
        }
      }
    })

    newGroups = (await Promise.all(newGroups)).filter((group) => group)

    let idx = 0;

    state.groups = state.groups.map((group) => {
      if(group.id === null){
        group.id = newGroups[idx].id
        group.students = newGroups[idx].students
        idx++
      }
      return group;
    })

    //Ajouter les groupes qui n'éxistaient pas dans la base de donnée
    newGroups.forEach((group) => {
        group.students.forEach((student) => {
            studentsToReassign.push({
                id_student: student.id,
                id_new_group: group.id
            })
        })
    })

    // Récupère les étudiants qui ne sont plus dans aucun groupe
    const oldGroupStudents = oldGroups.map((group) => group.students).flat();
    const newGroupStudents = state.groups.map((group) => group.students).flat();

    const studentsToDelete = oldGroupStudents.filter((student) => !newGroupStudents.some((newStudent) => newStudent.id === student.id));

    studentsToDelete.forEach((student) => {
        studentsToReassign.push({
            id_student: student.id,
            id_new_group: 0,
        })
    })

    if(studentsToReassign.length !== 0) {
      await reafectGroup(studentsToReassign);
    }

    toaster.showMessage("Groupes reaffectés avec succès", "success");
}

const handleDeleteGroup = async (group) => {
    state.groups = state.groups.filter((g) => g !== group);
}

const setDefaultPreferences = () => {
    const data ={
        "data": route.params.sessionId
    }
    const jsonData = JSON.stringify(data);

    axios.post(`${config.public.backUrl}/api/affect_default_preferencies`, jsonData, {
        headers: {
           'Content-Type': 'application/json'
        }}
    );
}

const validateGroups = async () => {
    if(getStudentsInGroup().length !== state.allStudents.length) {
      toaster.showMessage("Tout les étudiants doivent être affecter dans un groupe", "error");
      return
    }

    if(state.groups.length > stateProject.projects.length) {
      toaster.showMessage("Il ne peut pas y avoir plus de groupes que de projets", "error");
      return
    }

    const formData = {
        session_ID: route.params.sessionId,
        data: [
          {
            Nom: stateSession.session.name_session,
            Deadline_Creation_Groupe: stateSession.session.end_date_group,
            Deadline_Choix_Projet: stateSession.session.end_date_session,
            Nb_Etudiant_Min: stateSession.session.group_min,
            Nb_Etudiant_Max: stateSession.session.group_max,
            Etat: "Choosing",
            FK_Utilisateur: 1,
          },
        ],
      };

    const jsonDataSession = JSON.stringify(formData);
    await updateSession(jsonDataSession);
    await setDefaultPreferences();
    await sendGroupsMail();

    toaster.showMessage("Groupes attribués avec succès", "success");

    await navigateTo(`/session/${route.params.sessionId}`);
}

const sendGroupsMail = async () => {
    const formData = {
        session_ID: route.params.sessionId
    };
    const jsonData = JSON.stringify(formData);

    await axios.post(`${config.public.backUrl}/api/send_mail_group`, jsonData, {
        headers: {
            'Content-Type': 'application/json'
        }}
    );
}

const handleValidateGroup = async () => {
    if(!checkIfOneStudentInEachGroup()) return;
    await handleSave();
    await validateGroups();

}
</script>
