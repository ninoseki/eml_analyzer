<template>
  <div ref="root">
    <div class="box">
      <div class="upload-form">
        <b-message type="is-info" class="content">
          <ul>
            <li>EML(<code>.eml</code>) and MSG(<code>.msg</code>) formats are supported.</li>
            <li>
              The MSG file will be converted to the EML file before analyzing. The conversion might
              be lossy.
            </li>
            <li>This app doesn't store any information you enter.</li>
          </ul>
        </b-message>
        <b-field>
          <b-upload v-model="emlFile" drag-drop expanded>
            <section class="section">
              <div class="content has-text-centered">
                <p>
                  <b-icon icon="upload" size="is-large"></b-icon>
                </p>
                <p>Drop the EML/MSG file here or click to upload</p>
              </div>
            </section>
          </b-upload>
        </b-field>
        <div class="has-text-centered" v-if="emlFile">
          <b-button>{{ emlFile.name }}</b-button>
        </div>
      </div>
      <div class="has-text-centered">
        <b-button type="is-light" icon-pack="fas" icon-left="search" @click="analyze"
          >Analyze</b-button
        >
      </div>
    </div>
    <ResponseComponent :response="analyzeFileTask.last.value" v-if="analyzeFileTask.last?.value" />
  </div>
</template>

<script lang="ts">
import Vue from "vue"
import { onMounted, defineComponent, ref } from "vue"
import { useAsyncTask } from "vue-concurrency"

import { API } from "@/api"
import ResponseComponent from "@/components/Response.vue"
import { ErrorData, Response } from "@/types"
import { alertError } from "@/utils/alert"

export default defineComponent({
  name: "HomeView",
  components: {
    ResponseComponent
  },
  setup() {
    const buefy = Vue.prototype.$buefy
    const root = ref<HTMLElement>()
    const emlFile = ref<File | undefined>(undefined)

    const analyzeFileTask = useAsyncTask<Response, [File | undefined, String | undefined]>(
      async (_signal, file: File | undefined, identifier: String | undefined) => {
        if(identifier){
          return await API.lookupFile(identifier)
        } else {
          return await API.analyzeFile(file)
        }
      }
    )

    const lookup = async (fileIdentifier) => {
      const loadingComponent = buefy.loading.open({
        container: root.value
      })

      try {
        await analyzeFileTask.perform({"identifier": fileIdentifier })
        loadingComponent.close()
      } catch (error) {
        loadingComponent.close()

        const data = (error as any).response.data as ErrorData
        alertError(data, buefy)
      }
    }


    const analyze = async () => {
      const loadingComponent = buefy.loading.open({
        container: root.value
      })

      try {
        await analyzeFileTask.perform({"file": emlFile.value })
        loadingComponent.close()
      } catch (error) {
        loadingComponent.close()

        const data = (error as any).response.data as ErrorData
        alertError(data, buefy)
      }
    }

    onMounted(() => {
      const locationHash = location.hash;
      if(locationHash != ""){
        lookup(locationHash.substring(1));
      }
    })

    return { analyze, lookup, analyzeFileTask, emlFile, root }
  }
})
</script>

<style scoped>
.upload-form {
  margin-top: 20px;
  margin-bottom: 20px;
}
</style>
