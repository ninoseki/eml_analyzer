<template>
  <div @click="confirm">
    <span class="icon" @click="confirm">
      <img v-bind:src="submitter.favicon" alt="favicon" />
    </span>
    <span>{{ submitter.name }}</span>
  </div>
</template>

<script lang="ts">
import { Component, Mixins } from "vue-mixin-decorator";
import { Prop } from "vue-property-decorator";

import { ErrorDialogMixin } from "@/components/mixins/error_dialog";
import { Attachment, Submitter } from "@/types";
import { ErrorData } from "@/types";

@Component
export default class SubmitterComponent extends Mixins<ErrorDialogMixin>(
  ErrorDialogMixin
) {
  @Prop() private value!: Attachment;
  @Prop() private submitter!: Submitter;

  showResult(url: string): void {
    const message = `The submission result will be available at <a href="${url}" target="_blank">here</a>. Please wait for a while.`;
    this.$buefy.dialog.alert({
      title: "Submitted successfully",
      message: message,
      confirmText: "Close",
    });
  }

  confirm(): void {
    this.$buefy.dialog.confirm({
      message: `Are you sure to submit this attachment to ${this.submitter.name}?`,
      onConfirm: () => this.submit(),
    });
  }

  async submit(): Promise<void> {
    const loadingComponent = this.$buefy.loading.open({
      container: null,
    });

    try {
      const result = await this.submitter.submit(this.value);
      loadingComponent.close();

      this.showResult(result.referenceUrl);
    } catch (error) {
      loadingComponent.close();

      const data = error as ErrorData;
      this.alertError(data);
    }
  }
}
</script>

<style scoped>
img {
  margin-right: 5px;
}
</style>
