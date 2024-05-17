<template>
  <StudentsActions 
    title="GROUPE"
    :nb-steps="2"
    :nb-steps-active="1"
    :nb-steps-lock="1"
    sub-title="Renseignez les informations ci-dessous afin de créer votre demande de projet"
    button-title="Valider le groupe"
    @handle-button-click="validateGroup">
      <FormCreateGroup title="Votre groupe" subTitle="De qui est composé votre groupe ?" v-model:group="state.group"></FormCreateGroup>
  </StudentsActions>
</template>

<script setup>
import axios from 'axios';

const state = reactive({
  group: [],
})

const checkStudentIsInGroup = async (studentId) => {
    try {
      const res = await axios.post(
        "http://127.0.0.1:5000/api/student_is_in_group",
        {
          studentID: studentId
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      
      console.log(res)
      return res;
      } catch (err) {
        console.error(err);
      }
  }

  const checkStudentsInGroup = async () => {
    const promises = []
    
    state.group.forEach(student => {
      if(student){
        promises.push(checkStudentIsInGroup(student.id))
      }
    })

    return Promise.all(promises).then(res => {
      console.log(res)
      return res
    })
  }

  const createGroup = async () => {
    try {

      const data = {"data": state.group.map(student => {return {'studentID': student.id}})}

      const jsonData = JSON.stringify(data);

      await axios.post(
        "http://127.0.0.1:5000/api/create_group",
        jsonData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
    } catch (err) {
      console.error(err);
    }
  }
  

  const validateGroup = async () => {
    if(await checkStudentsInGroup()) {
      await createGroup(state.group) 
      await navigateTo('/createGroupConfirmation')
    }

   
  }
</script>
