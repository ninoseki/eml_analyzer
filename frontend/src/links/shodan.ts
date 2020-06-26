import { Link, LinkType } from "@/types";

export class Shodan implements Link {
  public baseURL: string;
  public favicon: string;
  public name: string;
  public type: LinkType;

  public constructor() {
    this.baseURL = "https://shodan.io";
    this.favicon = "https://www.google.com/s2/favicons?domain=shodan.io";
    this.name = "Shodan";
    this.type = "ip_address";
  }

  public href(value: string): string {
    return this.baseURL + `/host/${value}`;
  }
}
