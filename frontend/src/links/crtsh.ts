import { Link, LinkType } from "@/types";

export class Crtsh implements Link {
  public baseURL: string;
  public favicon: string;
  public name: string;
  public type: LinkType;

  public constructor() {
    this.baseURL = "https://crt.sh";
    this.favicon = "https://www.google.com/s2/favicons?domain=crt.sh";
    this.name = "crt.sh";
    this.type = "domain";
  }

  public href(value: string): string {
    return this.baseURL + `/?q=${value}`;
  }
}
