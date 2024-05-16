<template>
  <div>
    <NavBar :name="'fdsf'" />
    <div class="grid justify-center m-8">
      <FormSession editMode></FormSession>
      <div class="flex items-center mt-5 mb-5">
        <h2 class="text-3xl font-semibold mr-5">Projets</h2>
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
            @deleteProject="handleDeleteProject"
            id="1"
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
import axios from "axios";
const handleDeleteProject = (newProject) => {
  console.log("handleDeleteProject");
};
const state = reactive({
  editMode: false,
  name: null,
  summary: null,
  isOpen: false,
});
const create_project = async (jsonData) => {
  try {
    const res = await axios.post(
      "http://127.0.0.1:5000/api/create_project",
      jsonData,
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    return res;
  } catch (err) {
    console.error(err.response);
  }
};
const handleNewProject = async (newProject) => {
  console.log("handleNewProject", newProject);
  const formData = {
    data: [
      {
        Nom: "fdsfsdfs",
        Description: "desc",
        Nb_Etudiant_Min: null,
        Nb_Etudiant_Max: null,
        FK_Session: 1,
      },
    ],
  };
  const jsonDataSession = JSON.stringify(formData);
  const project_id = await create_project(jsonDataSession);

  console.log(project_id);
};
const handleModifyProject = (newProject) => {
  console.log("handleModifyProject", newProject);
};
const openCreateModal = () => {
  console.log("openCreateModal");
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
