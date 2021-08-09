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
    this.favicon =
      "https://www.google.com/s2/favicons?domain=securitytrails.com";
    this.type = "domain";
  }

  public href(value: string): string {
    return buildURL(this.baseURL, `/domain/${value}`);
  }
}
