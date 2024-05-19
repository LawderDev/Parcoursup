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
    
      const checkStudentsInGroup = async () => {
        const promises = []
        
        stateCreateGroup.group.forEach(student => {
          if(student){
            promises.push(checkStudentIsInGroup(student.id))
          }
        })
    
        return Promise.all(promises).then(res => {
          return res
        })
      }
    
      const createGroup = async () => {
        try {
    
          const data = {"data": stateCreateGroup.group.map(student => {return {'studentID': student.id}})}
    
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
          await createGroup(stateCreateGroup.group) 
        }
      }

      return {
          stateCreateGroup,
          validateGroup,
      }
}