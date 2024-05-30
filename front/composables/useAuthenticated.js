import axios from "axios";
import { useRoute } from "vue-router";
export async function useAuthenticated() {
  const getAuthenticated = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:5000/api/authenticated",
        { withCredentials: true }
      );
      return response.data;
    } catch (error) {
      console.error(
        "Erreur lors de la récupération de l'état de la connexion :",
        error
      );
      return error.response;
    }
  };

  const protectedRoutes = [
    "session-id",
    "index",
    "result-sessionId",
    "validateGroup-sessionId",
    "users",
  ];
  const route = useRoute();

  const verifyLogin = async () => {
    try {
      if (protectedRoutes.includes(route.name)) {
        const authStatus = await getAuthenticated();
        const isLogged = authStatus.status === "logged_in";
        if (!isLogged) {
          navigateTo("/login");
        }
      }
    } catch (error) {
      console.error(error);
      abortNavigation();
    }
  };
  return {
    verifyLogin,
  };
}
