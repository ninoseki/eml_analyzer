import { Link, LinkType } from "@/types";
import { buildURL } from "@/utils/urlBuilder";

class Urlscan implements Link {
  public favicon: string;
  public baseURL: string;
  public name: string;
  public type: LinkType;

  public constructor() {
    this.baseURL = "https://urlscan.io";
    this.favicon = "https://www.google.com/s2/favicons?domain=urlscan.io";
    this.name = "urlscan.io";
    this.type = "domain";
  }

  public href(value: string): string {
    return value;
  }
}

export class UrlscanForURL extends Urlscan {
  public constructor() {
    super();
    this.type = "url";
  }

  public href(value: string): string {
    const query = encodeURIComponent(`task.url:"${value}"`);
    return buildURL(this.baseURL, `/search/#${query}`);
  }
}

export class UrlscanForDomain extends Urlscan {
  public constructor() {
    super();
    this.type = "domain";
  }

  public href(value: string): string {
    return buildURL(this.baseURL, `/domain/${value}`);
  }
}

export class UrlscanForIP extends Urlscan {
  public constructor() {
    super();
    this.type = "ip_address";
  }

  public href(value: string): string {
    return buildURL(this.baseURL, `/ip/${value}`);
  }
}
