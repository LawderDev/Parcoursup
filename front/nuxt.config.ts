// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss', "@nuxt/image",'@pinia/nuxt', '@cssninja/nuxt-toaster'],
  transpile: ['@vuepic/vue-datepicker'],
  app: {
    head: {
      title: 'Smart choice',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { hid: 'description', name: 'description', content: 'Bienvenue sur Smart choice' }
      ],
    }
  }
})