<template>
  <div class="box">
    <article class="message is-info">
      <div class="message-body content">
        <ul>
          <li>EML(<code>.eml</code>) and MSG(<code>.msg</code>) formats are supported.</li>
          <li>
            The MSG file will be converted to the EML file before analyzing. The conversion might be
            lossy.
          </li>
          <li v-if="!status.cache">This app doesn't store EML/MSG file you upload.</li>
        </ul>
      </div>
    </article>
    <div class="field">
      <label class="upload control is-expanded">
        <div
          class="upload-draggable is-primary is-expanded"
          @dragover.prevent="updateDragDropFocus(true)"
          @dragleave.prevent="updateDragDropFocus(false)"
          @dragenter.prevent="updateDragDropFocus(true)"
          @drop.prevent="onFileChangeDrop"
        >
          <section class="section">
            <div class="content has-text-centered">
              <p>
                <span class="icon is-large">
                  <font-awesome-icon icon="upload"></font-awesome-icon>
                </span>
              </p>
              <p>Drop the EML/MSG file here or click to upload</p>
            </div>
          </section>
        </div>
        <input type="file" @change="onFileChange"
      /></label>
    </div>
    <div class="has-text-centered mt-3 mb-3" v-if="filename">
      <p>{{ filename }}</p>
    </div>
    <div class="has-text-centered">
      <button class="button is-light" @click="analyze">
        <span class="icon is-small">
          <font-awesome-icon icon="search"></font-awesome-icon>
        </span>
        <span>Analyze</span>
      </button>
    </div>
  </div>
  <Loading v-if="analyzeTask.isRunning"></Loading>
  <ErrorMessage :error="analyzeTask.last?.error" v-if="analyzeTask.isError" />
  <Response
    :response="analyzeTask.last.value"
    v-if="analyzeTask.last?.value && !analyzeTask.isRunning"
  />
</template>

<script lang="ts">
import { computed, defineComponent, ref, watch } from 'vue'
import { useAsyncTask } from 'vue-concurrency'

import { API } from '@/api'
import ErrorMessage from '@/components/ErrorMessage.vue'
import Loading from '@/components/Loading.vue'
import Response from '@/components/Response.vue'
import type { ResponseType } from '@/schemas'
import { useStatusStore } from '@/store'

export default defineComponent({
  name: 'UploadItem',
  components: {
    Response,
    ErrorMessage,
    Loading
  },
  setup() {
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

    return {
      analyze,
      analyzeTask,
      file,
      filename,
      updateDragDropFocus,
      onFileChangeDrop,
      onFileChange,
      dragDropFocus,
      status
    }
  }
})
</script>

<style scoped>
.upload {
  position: relative;
  display: inline-flex;
}

.upload input[type='file'] {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  outline: none;
  cursor: pointer;
  z-index: -1;
}

.upload .upload-draggable {
  cursor: pointer;
  padding: 0.25em;
  border: 1px dashed hsl(0, 0%, 71%);
  border-radius: 6px;
}

.upload .upload-draggable:hover {
  border-color: #7957d5;
  background: rgba(121, 87, 213, 0.05);
}

.upload .upload-draggable.is-expanded,
.upload.is-expanded {
  width: 100%;
}

.upload.is-rounded {
  border-radius: 9999px;
}

.upload.is-rounded .file-name {
  border-top-right-radius: 9999px;
  border-bottom-right-radius: 9999px;
}

@media screen and (-ms-high-contrast: active), screen and (-ms-high-contrast: none) {
  .upload input[type='file'] {
    z-index: auto;
  }

  .upload .upload-draggable + input[type='file'] {
    z-index: -1;
  }
}
</style>
