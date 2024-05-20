import axios from 'axios';

export function useGroups() {
    const stateGroups = reactive({
      groups: [],
    })
    
    const getAllGroups = async (sessionId) => {
        try {
          const data = {
            sessionID: sessionId
          }
    
          const jsonData = JSON.stringify(data);
    
          const res = await axios.post(
            "http://127.0.0.1:5000/api/get_all_groups_students",
            jsonData,
            {
              headers: {
                "Content-Type": "application/json",
              },
            }
          );
          
          stateGroups.groups = res.data
        } catch (err) {
          console.error(err);
        }
      }

      return {
          stateGroups,
          getAllGroups,
      }
}