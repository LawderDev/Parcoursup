<template>
    <div class="flex gap-4">
      <Combobox :value="selected" :default-value="defaultValue" @update:model-value="updateSelected">
        <div class="relative mt-1">
          <div
            class="relative w-full cursor-default rounded-full bg-base-100 text-left sm:text-sm"
          >
            <ComboboxInput
              class="w-[250px] rounded-full border-[1px] shadow-md py-2 pl-3 pr-10 text-sm leading-5"
              :displayValue="(person) => `${person.name} ${person.firstname}`"
              @change="state.query = $event.target.value"
            />
            <ComboboxButton
              class="absolute inset-y-0 right-0 flex items-center pr-2"
            >
              <img src="../public/people.svg" alt="people" class="h-5 w-5"/>
            </ComboboxButton>
          </div>
          <TransitionRoot
            leave="transition ease-in duration-100"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
            @after-leave="state.query = ''"
          >
            <ComboboxOptions
              class="absolute mt-1 max-h-60 w-full z-10 overflow-auto rounded-lg bg-base-100 py-1 text-base shadow-lg ring-1 ring-black/5 focus:outline-none sm:text-sm"
            >
              <div
                v-if="filteredPeople.length === 0 && state.query !== ''"
                class="relative cursor-default select-none px-4 py-2 text-secondary"
              >
                Nothing found.
              </div>
  
              <ComboboxOption
                v-for="person in filteredPeople"
                as="template"
                :key="person.id"
                :value="person"
                v-slot="{ selected, active }"
              >
                <li
                  class="relative cursor-default select-none py-2 pl-3 pr-4"
                  :class="{
                    'bg-primary text-base-100': active,
                    'text-secondary': !active,
                  }"
                >
                  <span
                    class="block truncate"
                    :class="{ 'font-medium': selected, 'font-normal': !selected }"
                  >
                    {{ person.name }} {{  person.firstname }}
                  </span>
                </li>
              </ComboboxOption>
            </ComboboxOptions>
          </TransitionRoot>
        </div>
      </Combobox>
      <button @click.prevent="$emit('delete')">
           <img src="@/public/minus.svg" alt="Image" class="w-6 h-6 mr-2">
        </button>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import {
    Combobox,
    ComboboxInput,
    ComboboxButton,
    ComboboxOptions,
    ComboboxOption,
    TransitionRoot,
  } from '@headlessui/vue'
  

  const props = defineProps({
      selected: Object,
      peoples: Array,
      defaultValue: Object,
  })

  const emit = defineEmits(['update:selected', 'delete'])

  const state = reactive({
      query: '',
  })


  onMounted(() => {
     emit('update:selected', props.defaultValue)
  })

  const updateSelected = (person) => {
    emit('update:selected', person)
  }

  let filteredPeople = computed(() =>
    state.query === ''
      ? props.peoples
      : props.peoples.filter((person) =>
      (person.name +
          person.firstname)
            .toLowerCase()
            .replace(/\s+/g, '')
            .includes(state.query.toLowerCase().replace(/\s+/g, ''))
        )
  )
  </script>
  