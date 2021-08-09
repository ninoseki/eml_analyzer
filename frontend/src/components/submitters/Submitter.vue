<template>
  <div @click="confirm">
    <span class="icon" @click="confirm">
      <img :src="submitter.favicon" alt="favicon" />
    </span>
    <span>{{ submitter.name }}</span>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "@vue/composition-api";

import { Attachment, ErrorData, Submitter } from "@/types";
import { alertError } from "@/utils/alert";

export default defineComponent({
  name: "Submitter",
  props: {
    value: {
      type: Object as PropType<Attachment>,
      required: true,
    },
    submitter: {
      type: Object as PropType<Submitter>,
      required: true,
    },
  },
  setup(props, context) {
    const showResult = (url: string) => {
      const message = `The submission result will be available at <a href="${url}" target="_blank">here</a>. Please wait for a while.`;
      context.root.$buefy.dialog.alert({
        title: "Submitted successfully",
        message: message,
        confirmText: "Close",
      });
    };

    const confirm = () => {
      context.root.$buefy.dialog.confirm({
        message: `Are you sure to submit this attachment to ${props.submitter.name}?`,
        onConfirm: () => submit(),
      });
    };

    const submit = async () => {
      const loadingComponent = context.root.$buefy.loading.open({
        container: null,
      });
      try {
        const result = await props.submitter.submit(props.value);
        loadingComponent.close();
        showResult(result.referenceUrl);
      } catch (error) {
        loadingComponent.close();
        const data = error as ErrorData;
        alertError(data, context);
      }
    };

    return { confirm };
  },
});
</script>

<style scoped>
img {
  margin-right: 5px;
}
</style>
