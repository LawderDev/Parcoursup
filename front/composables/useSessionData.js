import axios from 'axios';

export function useSessionData() {
    const config = useRuntimeConfig();

    const stateSession = reactive({
      session: null,
    })

    const getSessionData = async (sessionID) => {
        try {
        const response = await axios.get(
            `${config.public.backUrl}/api/get_session_data?sessionID=` + sessionID
        );
        if (response.data) {
            stateSession.session = response.data;
            return true;
        } else {
            return false;
        }
        } catch (error) {
        console.error("Erreur lors de la récupération des sessions :", error);
        }
    };

    const updateSession = async (jsonData) => {
        try {
          const res = await axios.post(`${config.public.backUrl}/api/update_session`, jsonData, {
            headers: {
              "Content-Type": "application/json",
            },
          });
          return res.data;
        } catch (err) {
          console.error(err);
        }
      }

    return {
       stateSession,
       getSessionData,
       updateSession,
    }
}

