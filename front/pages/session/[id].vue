<template>
  <div>
    <NavBar :name="'fdsf'" />
    <div class="grid justify-center m-8">
      <FormSession v-if="state.session_data" editMode :session-data="state.session_data"></FormSession>
      <div class="flex items-center mt-5 mb-5">
        <h2 class="text-3xl font-semiboldmr-5">Projets</h2>
        <ModalProjectForm
          v-model:isOpen="state.isOpen"
          :editMode="state.editMode"
          v-model:name="state.name"
          v-model:summary="state.summary"
          @submit:project="handleNewProject"
          @modify:project="handleModifyProject"
          @create:project="openCreateModal"
        >
        </ModalProjectForm>
        <ButtonPrimary class="ml-auto">Assigner les projets</ButtonPrimary>
      </div>

      <h3 class="ml-5 text-gray-500">Quels seront les projets disponibles ?</h3>
      <div
        class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 mb-20 md:mb-0"
      >
        <div v-for="item in liste" :key="item.id">
          <ProjectCard
            @modifyProject="openModifyModal"
            :name="item.name"
            :summary="item.summary"
          />
        </div>
      </div>
    </div>
    <!-- Boutons en bas de l'écran -->
  </div>
</template>

<script setup>
import { useRoute } from "vue-router";
import axios from "axios";
import { onMounted } from "vue";

const state = reactive({
  editMode: false,
  createProject: false,
  name: null,
  summary: null,
  isOpen: false,
  session_data: null,
});
const handleNewProject = (newProject) => {
  console.log("handleNewProject", newProject);
};
const handleModifyProject = (newProject) => {
  console.log("handleModifyProject", newProject);
};
const openCreateModal = (event) => {
  console.log("openCreateModal", event);
  state.isOpen = true;
  state.editMode = false;
  state.name = null;
  state.summary = null;
};
const openModifyModal = (event) => {
  console.log("openModifyModal", event.name);
  console.log("openModifyModal", event.summary);
  state.isOpen = true;
  state.editMode = true;
  state.name = event.name;
  state.summary = event.summary;
};

const route = useRoute();
const sessionID = route.params.id;

definePageMeta({
  validate: async (route) => {
    const api_check_id = async (sessionID) => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/api/get_session_id?sessionID=" + sessionID
        );

        if (!response.data || response.data.length == 0) {
          return false;
        } else {
          return true;
        }
      } catch (error) {
        console.error("Erreur lors de la récupération des sessions :", error);
      }
    };
    return (
      typeof route.params.id === "string" &&
      /^\d+$/.test(route.params.id) &&
      api_check_id(route.params.id)
    );
  },
});

const api_call_session_data = async (sessionID) => {
  try {
    const response = await axios.get(
      "http://127.0.0.1:5000/api/get_session_data?sessionID=" + sessionID
    );
    console.log(response.data);
    if (response.data) {
      state.session_data = response.data;
      return true;
    } else {
      return false;
    }
  } catch (error) {
    console.error("Erreur lors de la récupération des sessions :", error);
  }
};

onMounted( () => {
  api_call_session_data(sessionID)
})


const liste = [
  {
    id: 1,
    name: "Titre de l'élément 1",
    summary:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed quis ex non mauris vehicula scelerisque. Ut in ex ac nulla auctor dictum. Quisque volutpat vulputate risus, non scelerisque justo porta a. Phasellus auctor nisl vel tincidunt consequat. Suspendisse potenti. Nullam vestibulum malesuada faucibus. Suspendisse ac tortor lectus. Maecenas in pulvinar felis. Sed sit amet augue nec orci tincidunt lacinia. Vivamus euismod, metus ac convallis feugiat, libero elit auctor libero, nec vestibulum justo libero a dolor. Fusce efficitur libero eu justo suscipit, vitae finibus mi bibendum. Cras vulputate elit et lacus ultricies, vitae placerat enim vestibulum.",
  },
  {
    id: 2,
    name: "Titre de l'élément 2",
    summary:
      "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Integer id lorem sit amet purus ultrices consequat at et libero. Duis ultricies quam vitae diam scelerisque sollicitudin. Maecenas fermentum justo vel dui sodales dapibus. Etiam nec nulla vel odio aliquet facilisis. Vivamus ut est a enim consectetur consectetur. Nulla facilisi. Vivamus bibendum ultricies mi, nec suscipit felis malesuada ac. Ut tempus justo sapien, eu tincidunt turpis iaculis vel. Ut et magna nec libero commodo venenatis nec nec mauris. Nam eget vehicula odio, ut mattis ipsum. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Ut dapibus dui sed quam fermentum, sed fermentum lorem porttitor. Integer nec vestibulum lacus. Proin varius tempus velit, ut rhoncus mi varius id. Integer tristique leo nec velit fringilla, sed vehicula nunc rhoncus.",
  },
  {
    id: 3,
    name: "Titre de l'élément 3",
    summary:
      "Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Integer ut arcu ac est tempor malesuada. Morbi lacinia nulla nec justo feugiat, ac convallis odio auctor. Nulla in turpis lorem. Nam non nibh fermentum, lobortis mi ut, consequat nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Integer volutpat vestibulum lorem, id accumsan lorem efficitur sit amet. Morbi laoreet euismod elit, ut egestas eros aliquet eget. Integer auctor eros in mi facilisis vehicula. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Curabitur venenatis sem id massa rutrum, nec interdum eros auctor. Fusce non sapien nec justo consequat viverra. Integer aliquet, enim eget mattis ultricies, velit ipsum vulputate metus, eget pharetra justo tortor non odio. Aliquam rutrum nisi vel urna dapibus, sed fringilla velit suscipit. Aliquam erat volutpat. Cras vel metus nulla. Nam sed elit tincidunt, finibus lorem sit amet, lacinia ipsum.",
  },
  {
    id: 4,
    name: "Titre de l'élément 3",
    summary:
      "Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Integer ut arcu ac est tempor malesuada. Morbi lacinia nulla nec justo feugiat, ac convallis odio auctor. Nulla in turpis lorem. Nam non nibh fermentum, lobortis mi ut, consequat nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Integer volutpat vestibulum lorem, id accumsan lorem efficitur sit amet. Morbi laoreet euismod elit, ut egestas eros aliquet eget. Integer auctor eros in mi facilisis vehicula. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Curabitur venenatis sem id massa rutrum, nec interdum eros auctor. Fusce non sapien nec justo consequat viverra. Integer aliquet, enim eget mattis ultricies, velit ipsum vulputate metus, eget pharetra justo tortor non odio. Aliquam rutrum nisi vel urna dapibus, sed fringilla velit suscipit. Aliquam erat volutpat. Cras vel metus nulla. Nam sed elit tincidunt, finibus lorem sit amet, lacinia ipsum.",
  },
  {
    id: 5,
    name: "Titre de l'élément 3",
    summary:
      "Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Integer ut arcu ac est tempor malesuada. Morbi lacinia nulla nec justo feugiat, ac convallis odio auctor. Nulla in turpis lorem. Nam non nibh fermentum, lobortis mi ut, consequat nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Integer volutpat vestibulum lorem, id accumsan lorem efficitur sit amet. Morbi laoreet euismod elit, ut egestas eros aliquet eget. Integer auctor eros in mi facilisis vehicula. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Curabitur venenatis sem id massa rutrum, nec interdum eros auctor. Fusce non sapien nec justo consequat viverra. Integer aliquet, enim eget mattis ultricies, velit ipsum vulputate metus, eget pharetra justo tortor non odio. Aliquam rutrum nisi vel urna dapibus, sed fringilla velit suscipit. Aliquam erat volutpat. Cras vel metus nulla. Nam sed elit tincidunt, finibus lorem sit amet, lacinia ipsum.",
  },
];
</script>
