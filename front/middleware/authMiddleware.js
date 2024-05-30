import axios from "axios";
import { useAuthStore } from "~/stores/auth";

export default defineNuxtRouteMiddleware(async (to, from) => {
    const authStore = useAuthStore();
    const config = useRuntimeConfig();
    /*const getAuthenticated = async () => {
        try {
        const response = await axios.get(
            `${config.public.backUrl}/api/current_user`,
            { withCredentials: true }
        );
        return response.data;
        } catch (error) {
        console.error(
            "Erreur lors de la récupération de l'utilisateur connecté :",
            error
        );
        return null;
        }
    };*/

    const protectedRoutes = [
        "session-id",
        "index",
        "result-sessionId",
        "validateGroup-sessionId",
        "users",
    ];

    try {
        if (protectedRoutes.includes(to.name)) {
            /*const currentUser = await getAuthenticated();
            if (!currentUser) {
                return navigateTo("/login");
            }*/
            if(authStore.name === '' ||  authStore.firstName === '' ||  authStore.email === '') {
                return navigateTo("/login");
            }
        }
    } catch (error) {
        console.error(error);
        return abortNavigation()
    }
});
