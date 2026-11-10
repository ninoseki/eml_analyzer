import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it } from 'vitest'

import AttachmentItem from '@/components/attachments/AttachmentItem.vue'
import type { AttachmentType } from '@/schemas'

const attachment: AttachmentType = {
  raw: '',
  filename: 'test.txt',
  size: 2048,
  hash: { md5: 'dummy', sha1: 'dummy', sha256: 'dummy', sha512: 'dummy' },
  mimeType: 'text/plain',
  mimeTypeShort: 'text',
  contentHeader: {},
}

describe('AttachmentItem.vue', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders human-readable size', () => {
    const wrapper = mount(AttachmentItem, {
      props: { attachment },
      global: { stubs: { 'font-awesome-icon': true } },
    })

    const size = wrapper.findAll('tr').find((tr) => tr.find('th').text() === 'Size')
    expect(size?.find('td').text()).toBe('2.05 kB')
  })
})
