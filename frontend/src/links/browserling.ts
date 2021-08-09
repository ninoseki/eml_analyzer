import { Link, LinkType } from "@/types";
import { buildURL } from "@/utils/urlBuilder";

export class Browserling implements Link {
  public baseURL: string;
  public favicon: string;
  public name: string;
  public type: LinkType;

  public constructor() {
    this.baseURL = "https://www.browserling.com";
    this.favicon = "https://www.google.com/s2/favicons?domain=browserling.com";
    this.name = "Browserling";
    this.type = "url";
  }

  public href(value: string): string {
    return buildURL(
      this.baseURL,
      `/browse/win/7/ie/11/${encodeURIComponent(value)}`
    );
  }
}
