import { Link, LinkType } from "@/types";
import { buildURL } from "@/utils/urlBuilder";

export class Browserling implements Link {
  public baseURL: string;
  public favicon: string;
  public name: string;
  public type: LinkType;

  public constructor() {
    this.baseURL = "https://www.browserling.com";
    this.favicon = `https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=${this.baseURL}`;
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
