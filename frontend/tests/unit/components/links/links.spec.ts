import VueCompositionApi from "@vue/composition-api";
import { createLocalVue, shallowMount } from "@vue/test-utils";

import Links from "@/components/links/Links.vue";

const localVue = createLocalVue();
localVue.use(VueCompositionApi);

describe("Links.vue", () => {
  describe("#selectedLinks", () => {
    it("returns links which support domain", () => {
      const wrapper = shallowMount(Links, {
        localVue,
        propsData: { value: "example.com", type: "domain" },
      });

      const links = (wrapper.vm as any).selectedLinks;
      expect(links.length).toBeGreaterThan(0);

      links.forEach((link) => expect(link.type).toEqual("domain"));
    });
  });
});
