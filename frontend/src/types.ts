export interface Payload {
  file: File | null
}

export interface Hash {
  md5: string
  sha1: string
  sha256: string
  sha512: string
}

export interface HeaderItem {
  key: string
  values: (string | number)[]
}

interface Dictionary {
  [key: string]: (string | number)[]
}

export interface Attachment {
  raw: string
  filename: string
  size: number
  extension: string | null
  hash: Hash
  mimeType: string
  mimeTypeShort: string
  contentHeader: Dictionary
}

export interface Body {
  contentType: string | null
  hash: string
  contentHeader: Dictionary
  content: string
  urls: string[]
  emails: string[]
  domains: string[]
  ipAddresses: string[]
}

export interface Received {
  by: string[] | null
  date: string
  for: string[] | null
  from: string[] | null
  src: string
  with: string | null
  delay: number
}

export interface Header {
  messageId: string | null
  subject: string
  defect: string[] | null
  from: string | null
  to: string[]
  cc: string[] | null
  date: string
  receivedEmail: string[] | null
  receivedForemail: string[] | null
  receivedDomain: string[] | null
  receivedIp: string[] | null
  receivedSrc: string[] | null
  received: Received[] | null
  header: Dictionary
}

export interface Eml {
  attachments: Attachment[]
  bodies: Body[]
  header: Header
  id: string
}

export interface Detail {
  key: string
  score: number | null
  description: string
  referenceLink: string | null
}

export interface Verdict {
  name: string
  malicious: boolean
  score: number | null
  details: Detail[]
}

export interface Response {
  id: string
  eml: Eml
  verdicts: Verdict[]
}

export interface SubmissionResult {
  referenceUrl: string
  status: string | null
}

export interface ValidationError {
  loc: string[]
  msg: string
  type: string
}

export interface ErrorData {
  detail: string | ValidationError[]
}

export const securityKeys = [
  'received-spm',
  'authentication-results',
  'dkim-signature',
  'arc-authentication-results'
]

export const basicKeys = ['cc', 'date', 'from', 'message-id', 'received', 'subject', 'to']

export type LinkType = 'url' | 'email' | 'ip' | 'domain' | 'sha256'
export type IndicatorType = 'url' | 'email' | 'ip' | 'domain' | 'sha256'

export interface Link {
  name: string
  type: string
  baseURL: string
  favicon: string
  href(hostname: string): string
}

export type SubmitType = 'sha256'

export interface Submitter {
  name: string
  type: SubmitType
  favicon: string
  submit(attachment: Attachment): Promise<SubmissionResult>
}
