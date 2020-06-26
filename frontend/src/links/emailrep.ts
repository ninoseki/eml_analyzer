import { Link, LinkType } from "@/types";

export class EmailRep implements Link {
  public baseURL: string;
  public favicon: string;
  public name: string;
  public type: LinkType;

  public constructor() {
    this.baseURL = "https://emailrep.io";
    this.favicon = "https://www.google.com/s2/favicons?domain=emailrep.io";
    this.name = "EmailRepo";
    this.type = "email";
  }

  public href(value: string): string {
    return this.baseURL + `/${value}`;
  }
}
