<template>
  <div class="buttons links">
    <LinkComponent
      v-for="link in selectedLinks"
      v-bind:link="link"
      v-bind:value="value"
      v-bind:key="link.name"
    />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

import LinkComponent from "@/components/links/Link.vue";
import { Links } from "@/links";
import { Link, LinkType } from "@/types";

@Component({
  components: {
    LinkComponent,
  },
})
export default class LinksComponent extends Vue {
  @Prop() private value!: string;
  @Prop() private type!: LinkType;

  get selectedLinks(): Link[] {
    if (this.type === undefined) {
      return Links;
    }

    return Links.filter((link) => link.type === this.type);
  }
}
</script>
