import type { IndicatorType, LinkType } from '@/schemas'
import { buildURL } from '@/utils'

export class AnyRun implements LinkType {
  public baseURL: string
  public favicon: string
  public name: string
  public type: IndicatorType

  public constructor() {
    this.baseURL = 'https://app.any.run'
    this.favicon = `https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=${this.baseURL}`
    this.name = 'AnyRun'
    this.type = 'sha256'
  }

  public href(value: string): string {
    return buildURL(this.baseURL, `/submissions/#filehash:${value}`)
  }
}
