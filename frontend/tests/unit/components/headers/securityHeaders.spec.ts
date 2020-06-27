import { shallowMount } from "@vue/test-utils";

import SecurityHeaders from "@/components/headers/SecurityHeaders.vue";
import { secuirtyKeys } from "@/types";

import { header } from "../../fixtures";

describe("SecurityHeaders.vue", () => {
  describe("#securityHeaders", () => {
    it("returns security headers", () => {
      const wrapper = shallowMount(SecurityHeaders, {
        propsData: { header },
      });

      const headers = (wrapper.vm as any).securityHeaders;
      expect(headers.length).toBeGreaterThan(0);

      const keys = headers.map(
        (securityHeader) => securityHeader.key
      ) as string[];

      keys.forEach((key) => expect(secuirtyKeys).toContain(key));
    });
  });
});
