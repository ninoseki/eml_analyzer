import { Link, LinkType } from "@/types";

export class HybridAnalysis implements Link {
  public baseURL: string;
  public favicon: string;
  public name: string;
  public type: LinkType;

  public constructor() {
    this.baseURL = "https://www.hybrid-analysis.com";
    this.favicon =
      "https://www.google.com/s2/favicons?domain=hybrid-analysis.com";
    this.name = "Hybrid Analysis";
    this.type = "sha256";
  }

  public href(value: string): string {
    return this.baseURL + `/search?query=${value}`;
  }
}
