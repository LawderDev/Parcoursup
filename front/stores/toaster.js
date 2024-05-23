import { defineStore } from 'pinia'

export const useToasterStore = defineStore('alerts', {
    state: () => ({ message: '', type: '', isOpen: false, duration: 2500 }),

    actions: {
        showMessage(message, type = 'success') {
           this.message = message;
           this.type = type;
           this.isOpen = true;

           setTimeout(() => {
               this.isOpen = false;
           }, this.duration);
        },
    },
})