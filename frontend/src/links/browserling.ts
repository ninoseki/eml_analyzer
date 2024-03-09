import type { IndicatorType, LinkType } from '@/schemas'
import { buildURL } from '@/utils'

export class Browserling implements LinkType {
  public baseURL: string
  public favicon: string
  public name: string
  public type: IndicatorType

  public constructor() {
    this.baseURL = 'https://www.browserling.com'
    this.favicon = `https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=${this.baseURL}`
    this.name = 'Browserling'
    this.type = 'url'
  }

  public href(value: string): string {
    return buildURL(this.baseURL, `/browse/win/7/ie/11/${encodeURIComponent(value)}`)
  }
}
