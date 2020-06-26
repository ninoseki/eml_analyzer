import { sha256 } from "js-sha256";
import URL from "url-parse";

import { Link, LinkType } from "@/types";

class VirusTotal implements Link {
  public favicon: string;
  public baseURL: string;
  public name: string;
  public type: LinkType;

  public constructor() {
    this.name = "VirusTotal";
    this.baseURL = "https://www.virustotal.com";
    this.favicon = "https://www.google.com/s2/favicons?domain=virustotal.com";
    this.type = "url";
  }

  public href(value: string): string {
    return value;
  }
}

export class VirusTotalForSHA256 extends VirusTotal {
  public constructor() {
    super();
    this.type = "sha256";
  }

  public href(value: string): string {
    return this.baseURL + `/gui/file/${value}/detection`;
  }
}

export class VirusTotalForURL extends VirusTotal {
  public constructor() {
    super();
    this.type = "url";
  }

  private normalizeURL(uri: string): string {
    const parsedUrl = new URL(uri);
    if (parsedUrl.pathname === "/" && !uri.endsWith("/")) {
      return `${uri}/`;
    }
    return uri;
  }

  public href(value: string): string {
    const hash = sha256(this.normalizeURL(value));
    return this.baseURL + `/gui/url/${hash}/detection`;
  }
}

export class VirusTotalForDomain extends VirusTotal {
  public constructor() {
    super();
    this.type = "domain";
  }

  public href(value: string): string {
    return this.baseURL + `/gui/domain/${value}/detection`;
  }
}

export class VirusTotalForIP extends VirusTotal {
  public constructor() {
    super();
    this.type = "ip_address";
  }

  public href(value: string): string {
    return this.baseURL + `/gui/ip-address/${value}/details`;
  }
}
