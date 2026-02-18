import type { IndicatorType, LinkType } from '@/schemas'
import { buildURL } from '@/utils'

export class AbuseIPDB implements LinkType {
  public baseURL: string
  public favicon: string
  public name: string
  public type: IndicatorType

  public constructor() {
    this.baseURL = 'https://www.abuseipdb.com/'
    this.favicon = `https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=${this.baseURL}`
    this.name = 'AbuseIPDB'
    this.type = 'ip'
  }

  public href(value: string): string {
    return buildURL(this.baseURL, `/check/${value}`)
  }
}
