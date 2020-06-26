import { Link, LinkType } from "@/types";

export class AnyRun implements Link {
  public baseURL: string;
  public favicon: string;
  public name: string;
  public type: LinkType;

  public constructor() {
    this.baseURL = "https://app.any.run";
    this.favicon = "https://www.google.com/s2/favicons?domain=any.run";
    this.name = "AnyRun";
    this.type = "sha256";
  }

  public href(value: string): string {
    return this.baseURL + `/submissions/#filehash:${value}`;
  }
}
