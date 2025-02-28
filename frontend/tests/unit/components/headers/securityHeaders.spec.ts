import { shallowMount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import SecurityHeaders from '@/components/headers/SecurityHeaders.vue'
import { securityKeys } from '@/constants'

import { header } from '../../fixtures'

describe('SecurityHeaders.vue', () => {
  describe('#securityHeaders', () => {
    it('returns security headers', () => {
      const wrapper = shallowMount(SecurityHeaders, {
        propsData: { header }
      })

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const headers: any[] = (wrapper.vm as any).securityHeaders
      expect(headers.length).toBeGreaterThan(0)

      const keys = headers.map((securityHeader) => securityHeader.key) as string[]

      keys.forEach((key) => expect(securityKeys).toContain(key))
    })
  })
})
