import axios from 'axios';

export function useProject() {
    const config = useRuntimeConfig();

    const stateProject = reactive({
      projects: [],
    })

    const api_call_projects = async (sessionID) => {
        try {
          const data = {
            sessionID: sessionID,
          };
          const jsonData = JSON.stringify(data);
          const response = await axios.post(
            `${config.public.backUrl}/api/get_all_projects`,
            jsonData,
            {
              headers: {
                "Content-Type": "application/json",
              },
            }
          );
          stateProject.projects = response.data;
        } catch (error) {
          console.error("Erreur lors de la récupération des project :", error);
        }
      };

    return {
       stateProject,
       api_call_projects,
    }
}

