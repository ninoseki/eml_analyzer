<template>
  <div>
    <div class="box">
      <div class="upload-form">
        <b-message type="is-info" class="content">
          <VueMarkdown :source="informationMessages" />
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
        <b-button
          type="is-light"
          icon-pack="fas"
          icon-left="search"
          @click="parse"
          >Analyze</b-button
        >
      </div>
    </div>

    <ResponseComponent
      :response="analyzeFileTask.last.value"
      v-if="analyzeFileTask.last"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "@vue/composition-api";
import { useAsyncTask } from "vue-concurrency";
import VueMarkdown from "vue-markdown";

import { API } from "@/api";
import ResponseComponent from "@/components/Response.vue";
import { ErrorData, Response } from "@/types";
import { alertError } from "@/utils/alert";

export default defineComponent({
  name: "Home",
  components: {
    VueMarkdown,
    ResponseComponent,
  },

  setup(_, context) {
    const emlFile = ref<File | undefined>(undefined);

    const informationMessages = [
      "- EML(`.eml`) and MSG(`.msg`) formats are supported.",
      "  - The MSG file will be converted to the EML file before analyzing. The conversion might be lossy.",
      "- This app doesn't store any information you enter.",
    ].join("\n");

    const analyzeFileTask = useAsyncTask<Response, [File | undefined]>(
      async (_signal, file: File | undefined) => {
        return await API.analyzeFile(file);
      }
    );

    const parse = async () => {
      const loadingComponent = context.root.$buefy.loading.open({
        container: context.root.$el,
      });

      try {
        await analyzeFileTask.perform(emlFile.value);
        loadingComponent.close();
      } catch (error) {
        loadingComponent.close();

        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const data = (error as any).response.data as ErrorData;
        alertError(data, context);
      }
    };

    return { parse, analyzeFileTask, informationMessages, emlFile };
  },
});
</script>

<style scoped>
.upload-form {
  margin-top: 20px;
  margin-bottom: 20px;
}
</style>
