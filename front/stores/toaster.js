import { defineStore } from 'pinia'

export const useToasterStore = defineStore('alerts', {
    state: () => ({ message: '', type: '', isOpen: false }),

    actions: {
        showMessage(message, type = 'success') {
           this.message = message;
           this.type = type;
           this.isOpen = true;
        },
    },
})