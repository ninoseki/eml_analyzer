import type { IndicatorType, LinkType } from '@/schemas'
import { buildURL } from '@/utils'

class Urlscan implements LinkType {
  public favicon: string
  public baseURL: string
  public name: string
  public type: IndicatorType

  public constructor() {
    this.baseURL = 'https://urlscan.io'
    this.favicon = `https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=${this.baseURL}`
    this.name = 'urlscan.io'
    this.type = 'domain'
  }

  public href(value: string): string {
    return value
  }
}

export class UrlscanForURL extends Urlscan {
  public constructor() {
    super()
    this.type = 'url'
  }

  public href(value: string): string {
    const query = encodeURIComponent(`task.url:"${value}"`)
    return buildURL(this.baseURL, `/search/#${query}`)
  }
}

export class UrlscanForDomain extends Urlscan {
  public constructor() {
    super()
    this.type = 'domain'
  }

  public href(value: string): string {
    return buildURL(this.baseURL, `/domain/${value}`)
  }
}

export class UrlscanForIP extends Urlscan {
  public constructor() {
    super()
    this.type = 'ip'
  }

  public href(value: string): string {
    return buildURL(this.baseURL, `/ip/${value}`)
  }
}
