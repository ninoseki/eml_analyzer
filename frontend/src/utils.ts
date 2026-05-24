import dayjs from 'dayjs'
import duration from 'dayjs/plugin/duration'
import relativeTime from 'dayjs/plugin/relativeTime'
import utc from 'dayjs/plugin/utc'
import { isDomain, isEmail, isIPv4, isIPv6, isSHA256, isURL } from 'ioc-extractor'
import { Base64 } from 'js-base64'

dayjs.extend(utc)
dayjs.extend(duration)
dayjs.extend(relativeTime)

export function b64toBlob(b64data: string, contentType = '', sliceSize = 512): Blob {
  const byteCharacters = Base64.atob(b64data)
  const byteArrays: BlobPart[] = []

  for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
    const slice = byteCharacters.slice(offset, offset + sliceSize)
    const byteNumbers = Array.from({ length: slice.length }, (_, i) => slice.charCodeAt(i))
    const byteArray = new Uint8Array(byteNumbers)
    byteArrays.push(byteArray)
  }

  const blob = new Blob(byteArrays, { type: contentType })
  return blob
}

export function toCSV(values: string[]): string {
  return values.join(', ')
}

export function truncate(s: string, length: number, suffix = '...'): string {
  if (s.length <= length) {
    return s
  }
  return s.slice(0, Math.max(0, length - suffix.length)) + suffix
}

export function stringifyParams(params: Record<string, string | number | boolean>): string {
  const searchParams = new URLSearchParams()
  for (const [key, value] of Object.entries(params)) {
    searchParams.append(key, String(value))
  }
  return searchParams.toString()
}

export function buildURL(
  baseURL: string,
  path: string,
  params: Record<string, string | number | boolean> = {}
): string {
  const queryString = stringifyParams(params)
  if (queryString === '') {
    return `${baseURL}${path}`
  } else {
    return `${baseURL}${path}?${queryString}`
  }
}

export function base64fy(s: string): string {
  return Base64.encode(s).trim()
}

export function humanizeSeconds(seconds: number): string {
  if (seconds === 0) {
    return '-'
  }
  const duration = dayjs.duration(seconds, 'seconds')
  return duration.humanize(false)
}

export function toUTC(dt: string) {
  return dayjs.utc(dt).format()
}

export function getIndicatorType(value: string) {
  if (isURL(value)) {
    return 'url'
  }

  if (isEmail(value)) {
    return 'email'
  }

  if (isDomain(value)) {
    return 'domain'
  }

  if (isIPv4(value) || isIPv6(value)) {
    return 'ip'
  }

  if (isSHA256(value)) {
    return 'sha256'
  }

  return undefined
}
