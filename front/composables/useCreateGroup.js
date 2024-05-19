import axios from 'axios';

export function useCreateGroup() {
    const stateCreateGroup = reactive({
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
          
          return res;
          } catch (err) {
            console.error(err);
          }
      }
    
      const checkStudentsInGroup = async (group) => {
        const promises = []
        
        group.forEach(student => {
          if(student){
            promises.push(checkStudentIsInGroup(student.id))
          }
        })
    
        return Promise.all(promises).then(res => {
          return res
        })
      }
    
      const createGroup = async (group) => {
        try {
    
          const data = {"data": group.map(student => {return {'studentID': student.id}})}
    
          const jsonData = JSON.stringify(data);
    
          const res = await axios.post(
            "http://127.0.0.1:5000/api/create_group",
            jsonData,
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
      
    
      const validateGroup = async (group) => {
        if(await checkStudentsInGroup(group)) {
          return await createGroup(group) 
        }
      }

      return {
          stateCreateGroup,
          validateGroup,
      }
}