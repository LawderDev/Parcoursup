import axios from "axios";
import { useRuntimeConfig } from "#app";
import { useSessionData } from "~/composables/useSessionData";

export default defineNuxtRouteMiddleware(async (to, from) => {
  const config = useRuntimeConfig();
  const sessionID = to.params.sessionId
  console.log(sessionID)

  try {
    const { stateSession, getSessionData } = useSessionData()
    await getSessionData(sessionID)
    console.log(stateSession)

    const cutoffDate = new Date(stateSession.session.end_date_session);
    const currentDate = new Date();

    if (currentDate > cutoffDate || stateSession.session.state != "Choosing") {
      return navigateTo("/createGroup/closed");
    }
  } catch (error) {
    console.error("Failed to fetch cutoff date:", error);
    return abortNavigation()
  }
});
