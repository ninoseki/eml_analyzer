import type { SubmitterType } from '@/schemas'

import { InQuest } from './inquest'
import { VirusTotal } from './virustotal'

export const Submitters: SubmitterType[] = [new InQuest(), new VirusTotal()]
export { InQuest, VirusTotal }
