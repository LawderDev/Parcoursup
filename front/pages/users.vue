<template>
    <div>
      <NavBar></NavBar>
      <template v-if="state.isLoading">
        <div class="flex justify-end mr-10">
            <ModalCreateUser></ModalCreateUser>
        </div>
        <div class="mt-6">
          <UserItem
            v-for="user in state.users"
            :name="user.name"
            :firstname="user.firstname"
            @delete="openDeleteModal(user)"
            @handleClick="openUserPage(user.id)"
          ></UserItem>
        </div>
        <ModalDeleteUser hide-button v-model:isOpen="state.isOpen" :name="state.selectedUser.name" :firstname="state.selectedUser.firstname" :userId="state.selectedUser.id" @handle-delete="api_call_users"></ModalDeleteUser>
      </template>
      <Skeleton v-else></Skeleton>
    </div>
  </template>
  
  <script setup>
  import { reactive } from "vue";
  import axios from "axios";
  
  const config = useRuntimeConfig();
  
  const state = reactive({
    isOpen: false,
    selectedUser: {},
    users: [],
    isLoading: false
  });
  
  const openDeleteModal = (user) => {
    state.selectedUser.id = user.id;
    state.selectedUser.name = user.name;
    state.isOpen = true;
  };
  
  const openUserPage = async (userID) => {
    await navigateTo("/users/" + userID);
  };
  
  const api_call_users = async () => {
    try {
      const response = await axios.get(`${config.public.backUrl}/api/get_users`);
      state.users = response.data
      console.log(state.users)
    } catch (error) {
      console.error("Erreur lors de la récupération des utilisateurs :", error);
    }
    state.isOpen = false
  };

  onMounted(async () => {
    await api_call_users();
    state.isLoading = true;
  })
  
  
  </script>
  