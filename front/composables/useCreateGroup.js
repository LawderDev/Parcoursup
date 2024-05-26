import axios from 'axios';

export function useCreateGroup() {
    const stateCreateGroup = reactive({
      group: [],
    })
    
      const validateGroup = async (group) => {
        try {
          const data = {data: group.map(student => ({'studentID': student.id}))}
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
          return res
        } catch (err) {
          console.error(err);
        }
      }

      return {
          stateCreateGroup,
          validateGroup,
      }
}