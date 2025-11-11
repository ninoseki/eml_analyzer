<script setup lang="ts">
import truncate from 'just-truncate'
import { computed, onMounted, type PropType, ref } from 'vue'

import BodyComponent from '@/components/bodies/BodyItem.vue'
import type { AttachmentType, BodyType } from '@/schemas'

const props = defineProps({
  bodies: {
    type: Array as PropType<BodyType[]>,
    required: true
  },
  attachments: {
    type: Array as PropType<AttachmentType[]>,
    required: true
  }
})

const selectedBody = ref<BodyType>()
const selectedTabIndex = ref(0)
const inlineAttachments = computed(() => {
  const mapped = props.attachments.map((attachment) => {
    const contentId = attachment.contentId?.replace(/^<|>$/g, '')
    const data = `data:image/png;base64, ${attachment.raw}`
    if (contentId) {
      return [contentId, data]
    }
    return undefined
  })
  return Object.fromEntries(
    mapped.filter((entry) => entry !== undefined) as [string, string | undefined][]
  )
})

const select = (body: BodyType, index: number) => {
  selectedBody.value = body
  selectedTabIndex.value = index
}

onMounted(() => {
  if (props.bodies.length > 0) {
    selectedBody.value = props.bodies[0]
    selectedTabIndex.value = 0
  }
})
</script>

<template>
  <h2 class="text-2xl font-bold middle">Bodies</h2>
  <div role="tablist" class="tabs tabs-border justify-center">
    <a
      role="tab"
      class="tab"
      v-for="(body, index) in bodies"
      :class="{ 'tab-active': selectedTabIndex === index }"
      :key="body.hash"
      :body="body"
      @click="select(body, index)"
      >{{ truncate(body.contentType || index.toString(), 16) }}</a
    >
  </div>
  <BodyComponent :body="selectedBody" v-if="selectedBody" :inlineAttachments="inlineAttachments" />
</template>
