import { Link, LinkType } from "@/types";
import { buildURL } from "@/utils/urlBuilder";

export class InQuest implements Link {
  public baseURL: string;
  public favicon: string;
  public name: string;
  public type: LinkType;

  public constructor() {
    this.baseURL = "https://labs.inquest.net";
    this.favicon = `https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=${this.baseURL}`;
    this.name = "InQuest";
    this.type = "sha256";
  }

  public href(value: string): string {
    return buildURL(this.baseURL, `/dfi/sha256/${value}`);
  }
}
