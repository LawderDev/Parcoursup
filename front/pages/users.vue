<template>
    <div>
      <NavBar></NavBar>
      <template v-if="state.isLoading">
        <div class="flex justify-end mr-10">
            <ModalCreateUser @handle-validate="api_call_users"></ModalCreateUser>
        </div>
        <div class="mt-6">
          <UserItem
            v-for="user in state.users"
            :name="user.name"
            :firstname="user.firstname"
            @delete="openDeleteModal(user)"
            @handleClick="openEditModal(user)"
          ></UserItem>
        </div>
        <ModalDeleteUser hide-button v-model:isOpen="state.isDeleteOpen" :name="state.selectedUser.name" :firstname="state.selectedUser.firstname" :userId="state.selectedUser.id" @handle-delete="api_call_users"></ModalDeleteUser>
        <ModalEditUser v-model:isOpen="state.isEditOpen" :user="state.selectedUser" @handle-validate="api_call_users"></ModalEditUser>
      </template>
      <Skeleton v-else></Skeleton>
    </div>
  </template>
  
  <script setup>
  import { reactive } from "vue";
  import axios from "axios";
  
  const config = useRuntimeConfig();
  
  const state = reactive({
    isDeleteOpen: false,
    isEditOpen: false,
    selectedUser: {},
    users: [],
    isLoading: false
  });
  
  const openDeleteModal = (user) => {
    state.selectedUser = user;
    state.isDeleteOpen = true;
  };
  
  const openEditModal = async (user) => {
    state.selectedUser = user;
    state.isEditOpen = true;
  };
  
  const api_call_users = async () => {
    try {
      const response = await axios.get(`${config.public.backUrl}/api/get_users`);
      state.users = response.data
    } catch (error) {
      console.error("Erreur lors de la récupération des utilisateurs :", error);
    }
    state.isDeleteOpen = false;
    state.isEditOpen = false;
  };

  onMounted(async () => {
    await api_call_users();
    state.isLoading = true;
  })
  </script>
  