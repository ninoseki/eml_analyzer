<template>
  <div>
    <div class="box">
      <div class="upload-form">
        <b-message type="is-info" class="content">
          <VueMarkdown>
            - EML(`.eml`) and MSG(`.msg`) formats are supported.
          </VueMarkdown>
          <VueMarkdown
            >- This app doesn't store any information you enter.
          </VueMarkdown>
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

    <ResponseComponent v-bind:response="response" v-if="hasResponse" />
  </div>
</template>

<script lang="ts">
import axios from "axios";
import VueMarkdown from "vue-markdown";
import { Component, Mixins } from "vue-mixin-decorator";

import { ErrorDialogMixin } from "@/components/mixins/error_dialog";
import ResponseComponent from "@/components/Response.vue";
import { ErrorData, Response } from "@/types";

@Component({ components: { ResponseComponent, VueMarkdown } })
export default class Home extends Mixins<ErrorDialogMixin>(ErrorDialogMixin) {
  private emlFile: File | null = null;
  private response: Response | undefined = undefined;
  private hasResponse = false;

  async parse() {
    const loadingComponent = this.$buefy.loading.open({
      container: this.$el,
    });

    const formData = new FormData();
    if (this.emlFile !== null) {
      formData.append("file", this.emlFile);
    }

    this.response = undefined;
    this.hasResponse = false;

    try {
      const response = await axios.post<Response>(
        "/api/analyze/file",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      loadingComponent.close();

      this.response = response.data;
      this.hasResponse = true;
      this.$forceUpdate();
    } catch (error) {
      loadingComponent.close();

      const data = error.response.data as ErrorData;
      this.alertError(data);
    }
  }
}
</script>

<style scoped>
.upload-form {
  margin-top: 20px;
  margin-bottom: 20px;
}
</style>
