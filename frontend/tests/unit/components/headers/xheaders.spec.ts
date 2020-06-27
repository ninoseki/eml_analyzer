import { shallowMount } from "@vue/test-utils";

import XHeaders from "@/components/headers/XHeaders.vue";

import { header } from "../../fixtures";

describe("XHeaders.vue", () => {
  describe("#xHeaders", () => {
    it("returns headers which start with x", () => {
      const wrapper = shallowMount(XHeaders, {
        propsData: { header },
      });

      const headers = (wrapper.vm as any).xHeaders;
      expect(headers.length).toBeGreaterThan(0);

      headers.forEach((xHeader) =>
        expect(xHeader.key as string).toMatch(/^x-/)
      );
    });
  });
});
