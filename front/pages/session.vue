<template>
  <div>
    <NavBar :name="'fdsf'" />
    <div class="grid m-8 mx-10">
      <FormSession editMode></FormSession>
      <h3 class="ml-5 text-gray-500">Quels seront les projets disponibles ?</h3>
      <div class="grid grid-cols-1 md:grid-cols-4 mb-20 md:mb-0">
        <div v-for="item in liste" :key="item.id">
          <ProjectCard :title="item.title" :summary="item.summary" />
        </div>
      </div>
    </div>
    <!-- Boutons en bas de l'écran -->
  </div>
</template>

<script setup>
import { reactive } from "vue";
import Delete from "~/public/delete.svg";
const state = reactive({
  selectedFile: null,
  file: null,
  minGroup: 1,
  maxGroup: null,
  endDate: null,
  project: [""],
  error: false,
});
const handleDateSelected = (selectedDate) => {
  state.endDate = selectedDate;
};
const handleFileSelected = (file) => {
  state.selectedFile = file;
};

let formCorrect = computed(() => {
  return (
    fileCorrect.value &&
    dateCorrect.value &&
    groupCorrect.value &&
    projectCorrect.value
  );
});
const projectCorrect = computed(() => {
  return state.project != null && state.project.length > 0;
});
const fileCorrect = computed(() => {
  return state.selectedFile != null;
});
const dateCorrect = computed(() => {
  return state.endDate != null && new Date(state.endDate) >= new Date();
});
const groupCorrect = computed(() => {
  return (
    state.minGroup != null &&
    state.maxGroup != null &&
    state.minGroup > 0 &&
    state.maxGroup > state.minGroup
  );
});
const handleClick = () => {
  if (formCorrect.value) {
    console.log("valid form");
    state.error = false;
  } else {
    state.error = true;
  }
};
const liste = [
  {
    id: 1,
    title: "Titre de l'élément 1",
    summary:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed quis ex non mauris vehicula scelerisque. Ut in ex ac nulla auctor dictum. Quisque volutpat vulputate risus, non scelerisque justo porta a. Phasellus auctor nisl vel tincidunt consequat. Suspendisse potenti. Nullam vestibulum malesuada faucibus. Suspendisse ac tortor lectus. Maecenas in pulvinar felis. Sed sit amet augue nec orci tincidunt lacinia. Vivamus euismod, metus ac convallis feugiat, libero elit auctor libero, nec vestibulum justo libero a dolor. Fusce efficitur libero eu justo suscipit, vitae finibus mi bibendum. Cras vulputate elit et lacus ultricies, vitae placerat enim vestibulum.",
  },
  {
    id: 2,
    title: "Titre de l'élément 2",
    summary:
      "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Integer id lorem sit amet purus ultrices consequat at et libero. Duis ultricies quam vitae diam scelerisque sollicitudin. Maecenas fermentum justo vel dui sodales dapibus. Etiam nec nulla vel odio aliquet facilisis. Vivamus ut est a enim consectetur consectetur. Nulla facilisi. Vivamus bibendum ultricies mi, nec suscipit felis malesuada ac. Ut tempus justo sapien, eu tincidunt turpis iaculis vel. Ut et magna nec libero commodo venenatis nec nec mauris. Nam eget vehicula odio, ut mattis ipsum. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Ut dapibus dui sed quam fermentum, sed fermentum lorem porttitor. Integer nec vestibulum lacus. Proin varius tempus velit, ut rhoncus mi varius id. Integer tristique leo nec velit fringilla, sed vehicula nunc rhoncus.",
  },
  {
    id: 3,
    title: "Titre de l'élément 3",
    summary:
      "Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Integer ut arcu ac est tempor malesuada. Morbi lacinia nulla nec justo feugiat, ac convallis odio auctor. Nulla in turpis lorem. Nam non nibh fermentum, lobortis mi ut, consequat nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Integer volutpat vestibulum lorem, id accumsan lorem efficitur sit amet. Morbi laoreet euismod elit, ut egestas eros aliquet eget. Integer auctor eros in mi facilisis vehicula. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Curabitur venenatis sem id massa rutrum, nec interdum eros auctor. Fusce non sapien nec justo consequat viverra. Integer aliquet, enim eget mattis ultricies, velit ipsum vulputate metus, eget pharetra justo tortor non odio. Aliquam rutrum nisi vel urna dapibus, sed fringilla velit suscipit. Aliquam erat volutpat. Cras vel metus nulla. Nam sed elit tincidunt, finibus lorem sit amet, lacinia ipsum.",
  },
  {
    id: 4,
    title: "Titre de l'élément 3",
    summary:
      "Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Integer ut arcu ac est tempor malesuada. Morbi lacinia nulla nec justo feugiat, ac convallis odio auctor. Nulla in turpis lorem. Nam non nibh fermentum, lobortis mi ut, consequat nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Integer volutpat vestibulum lorem, id accumsan lorem efficitur sit amet. Morbi laoreet euismod elit, ut egestas eros aliquet eget. Integer auctor eros in mi facilisis vehicula. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Curabitur venenatis sem id massa rutrum, nec interdum eros auctor. Fusce non sapien nec justo consequat viverra. Integer aliquet, enim eget mattis ultricies, velit ipsum vulputate metus, eget pharetra justo tortor non odio. Aliquam rutrum nisi vel urna dapibus, sed fringilla velit suscipit. Aliquam erat volutpat. Cras vel metus nulla. Nam sed elit tincidunt, finibus lorem sit amet, lacinia ipsum.",
  },
  {
    id: 5,
    title: "Titre de l'élément 3",
    summary:
      "Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Integer ut arcu ac est tempor malesuada. Morbi lacinia nulla nec justo feugiat, ac convallis odio auctor. Nulla in turpis lorem. Nam non nibh fermentum, lobortis mi ut, consequat nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Integer volutpat vestibulum lorem, id accumsan lorem efficitur sit amet. Morbi laoreet euismod elit, ut egestas eros aliquet eget. Integer auctor eros in mi facilisis vehicula. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Curabitur venenatis sem id massa rutrum, nec interdum eros auctor. Fusce non sapien nec justo consequat viverra. Integer aliquet, enim eget mattis ultricies, velit ipsum vulputate metus, eget pharetra justo tortor non odio. Aliquam rutrum nisi vel urna dapibus, sed fringilla velit suscipit. Aliquam erat volutpat. Cras vel metus nulla. Nam sed elit tincidunt, finibus lorem sit amet, lacinia ipsum.",
  },
];
</script>
