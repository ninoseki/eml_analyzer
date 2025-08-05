<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useAsyncTask } from 'vue-concurrency'

import { API } from '@/api'
import Divider from '@/components/DividerItem.vue'
import ErrorMessage from '@/components/ErrorMessage.vue'
import Loading from '@/components/LoadingItem.vue'
import Response from '@/components/ResponseItem.vue'
import type { ResponseType } from '@/schemas'
import { useStatusStore } from '@/store'

const file = ref<File>()
const filename = ref<string>()
const dragDropFocus = ref(false)

const store = useStatusStore()
const status = computed(() => {
  return store.$state
})

const analyzeTask = useAsyncTask<ResponseType, [File]>(async (_signal, file: File) => {
  return await API.analyze(file)
})

const updateDragDropFocus = (value: boolean) => {
  dragDropFocus.value = value
}

const analyze = async () => {
  if (file.value) {
    await analyzeTask.perform(file.value)
  }
}

const onFileChangeDrop = (event: DragEvent) => {
  dragDropFocus.value = false
  if (event?.dataTransfer?.files) {
    file.value = event.dataTransfer.files[0]
  }
}

const onFileChange = (event: Event) => {
  const f = (event.target as HTMLInputElement).files?.[0]
  if (f) {
    file.value = f
  }
}

watch(file, () => {
  if (file.value) {
    filename.value = file.value.name
  }
})
</script>

<template>
  <div class="grid gap-4">
    <div class="alert border-info">
      <font-awesome-icon icon="info-circle" class="w-6 h-6 mr-2" />
      <ul class="list-disc list-inside space-y-1">
        <li>EML (<b>.eml</b>) and MSG (<b>.msg</b>) formats are supported.</li>
        <li>
          The MSG file will be converted to the EML file before analyzing. The conversion might be
          lossy.
        </li>
        <li v-if="!status.cache">This app doesn't store EML/MSG file you upload.</li>
      </ul>
    </div>
    <div
      class="w-full flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md upload-draggable"
      @dragover.prevent="updateDragDropFocus(true)"
      @dragleave.prevent="updateDragDropFocus(false)"
      @dragenter.prevent="updateDragDropFocus(true)"
      @drop.prevent="onFileChangeDrop"
    >
      <div class="text-center py-16">
        <p>
          <span class="text-4xl">
            <font-awesome-icon icon="upload"></font-awesome-icon>
          </span>
        </p>
        <p class="mt-4">Drop the EML/MSG file here or click to upload</p>
      </div>
      <input type="file" @change="onFileChange" />
    </div>
    <div class="text-center">
      <p class="mb-4" v-if="filename">{{ filename }}</p>
      <button class="btn btn-primary" @click="analyze">
        <font-awesome-icon icon="search" class="w-4 h-4"></font-awesome-icon>
        Analyze
      </button>
    </div>
  </div>
  <Divider />
  <Loading v-if="analyzeTask.isRunning" />
  <ErrorMessage :error="analyzeTask.last?.error" v-if="analyzeTask.isError" />
  <Response
    :response="analyzeTask.last.value"
    v-if="analyzeTask.last?.value && !analyzeTask.isRunning"
  />
</template>

<style scoped>
input[type='file'] {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  outline: none;
  cursor: pointer;
}

.upload-draggable {
  position: relative;
  cursor: pointer;
  padding: 0.25em;
  border: 1px dashed hsl(0, 0%, 71%);
  border-radius: 6px;
}

.upload-draggable:hover {
  border-color: #7957d5;
  background: rgba(121, 87, 213, 0.05);
}
</style>
