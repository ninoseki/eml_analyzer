import type { IndicatorType, Link } from '@/types'

export class EmailRep implements Link {
  public baseURL: string
  public favicon: string
  public name: string
  public type: IndicatorType

  public constructor() {
    this.baseURL = 'https://emailrep.io'
    this.favicon = `https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=${this.baseURL}`
    this.name = 'EmailRep'
    this.type = 'email'
  }

  public href(value: string): string {
    return this.baseURL + `/${value}`
  }
}
