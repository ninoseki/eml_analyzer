import { createLocalVue, shallowMount } from "@vue/test-utils"
import { describe, expect, it } from "vitest"

import XHeaders from "@/components/headers/XHeaders.vue"

import { header } from "../../fixtures"

const localVue = createLocalVue()

describe("XHeaders.vue", () => {
  describe("#xHeaders", () => {
    it("returns headers which start with x", () => {
      const wrapper = shallowMount(XHeaders, {
        localVue,
        propsData: { header }
      })

      const headers = (wrapper.vm as any).xHeaders
      expect(headers.length).toBeGreaterThan(0)

      headers.forEach((xHeader) => expect(xHeader.key as string).toMatch(/^x-/))
    })
  })
})
