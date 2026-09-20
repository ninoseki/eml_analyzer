import { shallowMount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";

import Content from "@/components/bodies/ContentItem.vue";

describe("Content.vue", () => {
  it("returns html", () => {
    const wrapper = shallowMount(Content, {
      props: {
        content: "foo",
        contentType: "text/html",
        inlineAttachments: {},
      },
    });
    expect(wrapper.find("iframe").exists()).toBe(true);
  });
});
