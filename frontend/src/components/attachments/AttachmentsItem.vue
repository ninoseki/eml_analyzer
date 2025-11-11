<script setup lang="ts">
import truncate from 'just-truncate'
import { onMounted, type PropType, ref } from 'vue'

import Attachment from '@/components/attachments/AttachmentItem.vue'
import type { AttachmentType } from '@/schemas'

const props = defineProps({
  attachments: {
    type: Array as PropType<AttachmentType[]>,
    required: true
  }
})

const selectedAttachment = ref<AttachmentType>()
const selectedTabIndex = ref(0)

const select = (attachment: AttachmentType, index: number) => {
  selectedAttachment.value = attachment
  selectedTabIndex.value = index
}

onMounted(() => {
  if (props.attachments.length > 0) {
    selectedAttachment.value = props.attachments[0]
    selectedTabIndex.value = 0
  }
})
</script>

<template>
  <h2 class="text-2xl font-bold middle">Attachments</h2>
  <div role="tablist" class="tabs tabs-border justify-center">
    <a
      role="tab"
      class="tab"
      v-for="(attachment, index) in attachments"
      :class="{ 'tab-active': selectedTabIndex === index }"
      :key="attachment.hash.md5"
      :attachment="attachment"
      @click="select(attachment, index)"
      >{{ truncate(attachment.filename, 16) }}</a
    >
  </div>
  <Attachment :attachment="selectedAttachment" v-if="selectedAttachment" />
</template>
