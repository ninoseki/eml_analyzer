<template>
  <div>
    <div class="box">
      <b-message type="is-info">
        This app doesn't store any information you enter.
      </b-message>
      <b-field label="EML file">
        <b-input
          class="is-expanded"
          type="textarea"
          rows="20"
          placeholder="Paste an EML file in here."
          v-model="emlFile"
        ></b-input>
      </b-field>

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
import { Component, Mixins } from "vue-mixin-decorator";

import { ErrorDialogMixin } from "@/components/mixins/error_dialog";
import ResponseComponent from "@/components/Response.vue";
import { ErrorData, Payload, Response } from "@/types";

@Component({ components: { ResponseComponent } })
export default class Home extends Mixins<ErrorDialogMixin>(ErrorDialogMixin) {
  private emlFile = "";
  private response: Response | undefined = undefined;
  private hasResponse = false;

  async parse() {
    const loadingComponent = this.$buefy.loading.open({
      container: this.$el,
    });

    const payload: Payload = {
      emlFile: this.emlFile,
    };

    this.response = undefined;
    this.hasResponse = false;

    try {
      const response = await axios.post<Response>("/api/analyze/", payload);

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
