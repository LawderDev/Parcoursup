import axios from 'axios';

export function useGroups() {
    const config = useRuntimeConfig()

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
            `${config.public.backUrl}/api/get_all_groups_students`,
            jsonData,
            {
              headers: {
                "Content-Type": "application/json",
              },
            }
          );
          
          console.log(res.data)
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