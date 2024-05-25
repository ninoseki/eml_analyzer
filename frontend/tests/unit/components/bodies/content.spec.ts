import { shallowMount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import Content from '@/components/bodies/ContentItem.vue'

describe('Content.vue', () => {
  it('returns html', () => {
    const wrapper = shallowMount(Content, {
      propsData: { content: 'foo', contentType: 'text/html' }
    })
    expect(wrapper.find('code.html'))
  })
})
