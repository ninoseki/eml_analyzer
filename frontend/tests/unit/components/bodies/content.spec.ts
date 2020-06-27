import { shallowMount } from "@vue/test-utils";

import Content from "@/components/bodies/Content.vue";

describe("Content.vue", () => {
  describe("#codeType", () => {
    it("returns plaintext", () => {
      const wrapper = shallowMount(Content, {
        propsData: { content: "foo", contentType: "text/plain" },
      });
      expect(wrapper.find("code.plaintext"));
    });

    it("returns html", () => {
      const wrapper = shallowMount(Content, {
        propsData: { content: "foo", contentType: "text/html" },
      });
      expect(wrapper.find("code.html"));
    });
  });
});
