import { Link, LinkType } from "@/types";
import { buildURL } from "@/utils/urlBuilder";

export class SecurityTrails implements Link {
  public favicon: string;
  public baseURL: string;
  public name: string;
  public type: LinkType;

  public constructor() {
    this.name = "SecurityTrails";
    this.baseURL = "https://securitytrails.com";
    this.favicon = `https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=${this.baseURL}`;
    this.type = "domain";
  }

  public href(value: string): string {
    return buildURL(this.baseURL, `/domain/${value}`);
  }
}
