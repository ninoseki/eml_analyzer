import type { IndicatorType, Link } from '@/types'
import { buildURL } from '@/utils'

export class Crtsh implements Link {
  public baseURL: string
  public favicon: string
  public name: string
  public type: IndicatorType

  public constructor() {
    this.baseURL = 'https://crt.sh'
    this.favicon = `https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=${this.baseURL}`
    this.name = 'crt.sh'
    this.type = 'domain'
  }

  public href(value: string): string {
    return buildURL(this.baseURL, '/', { q: value })
  }
}
