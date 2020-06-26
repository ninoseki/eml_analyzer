export interface Payload {
  emlFile: string;
}

export interface Hash {
  md5: string;
  sha1: string;
  sha256: string;
  sha512: string;
}

export interface HeaderItem {
  key: string;
  values: (string | number)[];
}

interface Dictionary {
  [key: string]: (string | number)[];
}

export interface Attachment {
  filename: string;
  size: number;
  extension: string;
  hash: Hash;
  mimeType: string;
  mimeTypeShort: string;
  contentHeader: Dictionary;
}

export interface Body {
  contentType: string | undefined;
  hash: string;
  contentHeader: Dictionary;
  content: string;
  urls: string[];
  emails: string[];
  domains: string[];
  ipAddresses: string[];
}

export interface Received {
  by: string[];
  date: string;
  for: string[];
  from: string[] | undefined;
  src: string;
  with: string;
}

export interface Header {
  messageId: string | undefined;
  subject: string;
  defect: string[] | undefined;
  from: string;
  to: string[];
  cc: string[];
  date: string;
  receivedEmail: string[] | undefined;
  receivedForemail: string[] | undefined;
  receivedDomain: string[] | undefined;
  receivedIp: string[] | undefined;
  receivedSrc: string[] | undefined;
  received: Received[] | undefined;
  header: Dictionary;
}

export interface Eml {
  attachments: Attachment[];
  bodies: Body[];
  header: Header;
}

export interface Detail {
  key: string;
  score: number | undefined;
  description: string;
}

export interface Verdict {
  name: string;
  malicious: boolean;
  score: number | undefined;
  details: Detail[];
}

export interface Response {
  eml: Eml;
  verdicts: Verdict[];
}

export interface ValidationError {
  loc: string[];
  msg: string;
  type: string;
}

export interface ErrorData {
  detail: string | ValidationError[];
}

export const secuirtyKeys = [
  "received-spm",
  "authentication-results",
  "dkim-signature",
  "arc-authentication-results",
];

export const basicKeys = [
  "cc",
  "date",
  "from",
  "message-id",
  "received",
  "subject",
  "to",
];

export type LinkType = "url" | "email" | "ip_address" | "domain" | "sha256";

export interface Link {
  name: string;
  type: string;
  baseURL: string;
  favicon: string;
  href(hostname: string): string;
}
