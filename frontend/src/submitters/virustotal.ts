import axios from 'axios'

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
    const res = await axios.post<SubmissionResultType>('/api/submit/virustotal', attachment)
    return res.data
  }
}
