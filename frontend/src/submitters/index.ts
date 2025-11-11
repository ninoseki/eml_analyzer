import type { SubmitterType } from '@/schemas'

import { VirusTotal } from './virustotal'

export const Submitters: SubmitterType[] = [new VirusTotal()]
export { VirusTotal }
