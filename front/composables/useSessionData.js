import axios from 'axios';

export function useSessionData() {
    const stateSession = reactive({
      session: null,
    })


    const getSessionData = async (sessionID) => {
        try {
        const response = await axios.get(
            "http://127.0.0.1:5000/api/get_session_data?sessionID=" + sessionID
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
          const res = await axios.post("http://127.0.0.1:5000/api/update_session", jsonData, {
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

