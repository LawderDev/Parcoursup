<template>
    <div id="container" class="pointer-events-none">
        <div class="toast toast-top toast-end z-[1000] transition-opacity ease-in-out" :class="{'opacity-0': !isOpen}">
            <div class="alert" :class="getType()">
                <span>{{ message }}.</span>
                <button
                    ref="crossBtn"
                    @click="toaster.isOpen = false"
                    class="btn btn-sm btn-circle btn-ghost border-1 border-black"
                    :class="isOpen ? 'pointer-events-auto' : 'pointer-events-none'"
                    >
                    ✕
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useToasterStore } from '@/stores/toaster';

const toaster = useToasterStore();

const props =defineProps({
    message: String,
    isOpen: Boolean,
    type: String,
})

const getType = () => {
    switch (props.type) {
        case 'success':
            return 'alert-success';
        case 'error':
            return 'alert-error';
        default:
            return 'alert-info';
    }
}
</script>

<style scoped>
.alert-success{
    @apply bg-primary text-white;
}

.alert-success button{
    @apply border-white;
}
</style>
