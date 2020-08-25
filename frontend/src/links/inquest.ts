import { Link, LinkType } from "@/types";
import { buildURL } from "@/utils/url_builder";

export class InQuest implements Link {
  public baseURL: string;
  public favicon: string;
  public name: string;
  public type: LinkType;

  public constructor() {
    this.baseURL = "https://labs.inquest.net";
    this.favicon = "https://www.google.com/s2/favicons?domain=inquest.net";
    this.name = "InQuest";
    this.type = "sha256";
  }

  public href(value: string): string {
    return buildURL(this.baseURL, `/dfi/sha256/${value}`);
  }
}
