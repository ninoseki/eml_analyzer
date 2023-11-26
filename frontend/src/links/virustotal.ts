import { sha256 } from "js-sha256"
import URL from "url-parse"

import { Link, LinkType } from "@/types"
import { buildURL } from "@/utils/urlBuilder"

class VirusTotal implements Link {
  public favicon: string
  public baseURL: string
  public name: string
  public type: LinkType

  public constructor() {
    this.name = "VirusTotal"
    this.baseURL = "https://www.virustotal.com"
    this.favicon = `https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=${this.baseURL}`
    this.type = "url"
  }

  public href(value: string): string {
    return value
  }
}

export class VirusTotalForSHA256 extends VirusTotal {
  public constructor() {
    super()
    this.type = "sha256"
  }

  public href(value: string): string {
    return buildURL(this.baseURL, `/gui/file/${value}/details`)
  }
}

export class VirusTotalForURL extends VirusTotal {
  public constructor() {
    super()
    this.type = "url"
  }

  private normalizeURL(uri: string): string {
    const parsedUrl = new URL(uri)
    if (parsedUrl.pathname === "/" && !uri.endsWith("/")) {
      return `${uri}/`
    }
    return uri
  }

  public href(value: string): string {
    const hash = sha256(this.normalizeURL(value))
    return buildURL(this.baseURL, `/gui/url/${hash}/details`)
  }
}

export class VirusTotalForDomain extends VirusTotal {
  public constructor() {
    super()
    this.type = "domain"
  }

  public href(value: string): string {
    return buildURL(this.baseURL, `/gui/domain/${value}/details`)
  }
}

export class VirusTotalForIP extends VirusTotal {
  public constructor() {
    super()
    this.type = "ip_address"
  }

  public href(value: string): string {
    return buildURL(this.baseURL, `/gui/ip-address/${value}/details`)
  }
}
