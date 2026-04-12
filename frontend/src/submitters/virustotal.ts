import { FetchError } from '@/api'
import type { AttachmentType, SubmissionResultType, SubmitterType, SubmitType } from '@/schemas'

export class VirusTotal implements SubmitterType {
  public favicon: string
  public name: string
  public type: SubmitType

  public constructor() {
    this.favicon = 'https://www.google.com/s2/favicons?domain=virustotal.com'
    this.name = 'VirusTotal'
    this.type = 'sha256'
  }

  public async submit(attachment: AttachmentType): Promise<SubmissionResultType> {
    const res = await fetch('/api/submit/virustotal', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(attachment)
    })
    if (!res.ok) {
      let data: unknown
      try {
        data = await res.json()
      } catch {
        // no JSON body
      }
      throw new FetchError(res.statusText, data)
    }
    return res.json()
  }
}
