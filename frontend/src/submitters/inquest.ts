import axios from "axios"

import { Attachment, SubmissionResult, Submitter, SubmitType } from "@/types"

export class InQuest implements Submitter {
  public favicon: string
  public name: string
  public type: SubmitType

  public constructor() {
    this.favicon = "https://www.google.com/s2/favicons?domain=inquest.net"
    this.name = "InQuest"
    this.type = "sha256"
  }

  public async submit(attachment: Attachment): Promise<SubmissionResult> {
    const res = await axios.post<SubmissionResult>("/api/submit/inquest", attachment)
    return res.data
  }
}
