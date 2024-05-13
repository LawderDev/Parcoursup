import Autocomplete from '@trevoreyre/autocomplete-vue'

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.component('autocomplete', Autocomplete);
})